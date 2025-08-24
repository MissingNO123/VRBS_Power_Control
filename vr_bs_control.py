from os.path import exists
import asyncio
import time
from bleak import BleakScanner, BleakClient, BleakError
import argparse
from sys import platform

parser = argparse.ArgumentParser(description="Control the power state of your HTC Vive Base Stations")
parser.add_argument("state", metavar="STATE", nargs="?", const="ON", help="Either on or off, default: on")
parser.add_argument("-s", "--save", action="store_true", help="Save addresses of Base Stations, skips scanning for devices every run")
parser.add_argument("-d", "--dryrun", action="store_true", help="Run the program without sending any Bluetooth commands")
args = parser.parse_args()

saved_addrs = []

if not args.save:
    if exists("basestations.txt"):
        r = open("basestations.txt", "r")
        saved_addrs = r.read().split(" ")
        print("Loaded %d saved basestations" % len(saved_addrs))

PowerState = True
if args.state:
    if args.state.lower() == "on": PowerState = True
    elif args.state.lower() == "off": PowerState = False

v1_Power_UUID = "0000cb00-0000-1000-8000-00805f9b34fb"
v1_Power_Char = "0000cb01-0000-1000-8000-00805f9b34fb"

CMD_ON  = b"\x12\x00\x00\x28\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
CMD_OFF = b"\x12\x01\x00\x28\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

v2_Power_UUID = "00001523-1212-efde-1523-785feabcd124"
v2_Power_Char = "00001525-1212-efde-1523-785feabcd124"

CMD_ON_V2 = b"\x01"
CMD_OFF_V2 = b"\x00"


async def powerState(bs, state):
    try:
        async with BleakClient(bs) as client:
            print("~ Connecting to %s... ~" % bs)
            while client.is_connected is False:
                time.sleep(0.05)
            print("Connected!")
            print("Powering %s..." % ("ON" if PowerState else "OFF"))
            # check if V2 BS Power Characteristic is available (by trying to write to it)
            try:
                cmd = CMD_ON_V2 if state else CMD_OFF_V2
                p = await client.read_gatt_char(v2_Power_Char)
                p = await client.write_gatt_char(v2_Power_Char, cmd)
            # if V2 Power Characteristic is not available that means it's probably a V1 BS
            except BleakError:  
                try:
                    cmd = CMD_ON if state else CMD_OFF
                    p = await client.read_gatt_char(v1_Power_Char)
                    p = await client.write_gatt_char(v1_Power_Char, cmd)
                except BleakError:
                    # In case some random device with the same name as a BS gets caught by the scan
                    print( "Cannot send command to %s, it is probably NOT a base station", bs )
            print("~ Disconnecting from %s... ~" % bs)
            await client.disconnect()
    except BleakError as e:
        print("Unable to connect to device: \n{}".format(e))


async def main():
    basestations = []
    tasks = []

    # Skip scanning if BSes already saved
    if len(saved_addrs):
        basestations = saved_addrs

    # Scan for any nearby BSes
    else:
        print("Scanning...")
        devices = await BleakScanner.discover()
        if len(devices) == 0:
            print("No devices found.")
            quit()
        for d in devices:
            if d.name is not None and (d.name.startswith("HTC BS ") or d.name.startswith("LHB-")):
                print("Found Base Station: %s" % d.name)
                basestations.append(d)
        if len(basestations) == 0:
            print("No base stations found.")
            quit()
        print("~~~")
        if args.save:  # Save BSes addresses to text file
            with open("basestations.txt", "w") as f:
                addresses = list([bs.address for bs in basestations])
                f.write(" ".join(addresses))
                print("Saved %d addresses" % len(addresses))

    # Connect to all BSes in parallel (might be stupid if you have >2 BSes, untested)
    if not args.dryrun:
        print( "Attempting to toggle power state to " + ( "ON" if PowerState else "OFF" ) + " for all base stations..." )
        
        #linux cannot connect to multiple devices at once, so we do it sequentially
        if platform.startswith("linux"):
            for bs in basestations:
                await powerState(bs, PowerState)
            print("Done!")
            return
        else:
            for bs in basestations:
                # await powerState(bs, PowerState)
                task = asyncio.create_task(powerState(bs, PowerState))
                tasks.append(task)
            await asyncio.gather(*tasks)
    print("Done!")

asyncio.run(main())
