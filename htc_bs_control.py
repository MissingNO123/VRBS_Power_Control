import asyncio
import time
import bleak
from bleak import BleakScanner, BleakClient, BleakError
import argparse

parser = argparse.ArgumentParser(description='Control the power state of your HTC Vive Base Stations')
parser.add_argument('state', metavar='STATE', nargs='?', const='ON', help='either on or off, default: on')
args = parser.parse_args()

PowerState = True
if args.state is None: PowerState = True
elif args.state.lower() == 'off': PowerState = False

v1_Power_UUID = "0000cb00-0000-1000-8000-00805f9b34fb"
v1_Power_Char = "0000cb01-0000-1000-8000-00805f9b34fb"

CMD_ON  = b"\x12\x00\x00\x28\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
CMD_OFF = b"\x12\x01\x00\x28\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

v2_Power_UUID = "00001523-1212-efde-1523-785feabcd124"
v2_Power_Char = "00001525-1212-efde-1523-785feabcd124"

CMD_ON_V2 = b"\x01"
CMD_OFF_V2 = b"\x00"

basestations = []

async def powerState(bs, value):
    async with BleakClient(bs) as client:
        print("~%s~" % bs.name)
        print("Connecting...")
        while client.is_connected is False:
            time.sleep(0.05)
        print("Connected!")
        print("Powering %s..." % "ON " if PowerState is True else "OFF")
        try: 
            cmd = CMD_ON_V2 if value else CMD_OFF_V2
            p = await client.read_gatt_char(v2_Power_Char) #check if V2 BS Power Characteristic is available
            p = await client.write_gatt_char(v2_Power_Char, cmd)
        except BleakError: #if V2 Power Characteristic is not available that means it's probably a V1 BS
            try: 
                cmd = CMD_ON if value else CMD_OFF
                p = await client.read_gatt_char(v1_Power_Char)
                p = await client.write_gatt_char(v1_Power_Char, cmd)
            except BleakError:
                print("Cannot send command to %s, it is probably NOT a base station", bs.name) # In case some random device with the same name as a BS gets caught by the scan
                return None
        print("Disconnecting...")
        return await client.disconnect()

async def main():
    print("Scanning...")
    devices = await BleakScanner.discover()
    if len(devices) == 0:
        print("No devices found.")
        quit()
    for d in devices:
        if d.name is not None and d.name.startswith('HTC BS '):
            print("Found Base Station: %s" % d.name)
            basestations.append(d) 
    if len(basestations) == 0:
        print("No base stations found.")
        quit()
    print("~~~")
    for bs in basestations:
        await powerState(bs, PowerState)
        print("~~~")
    print("Done!")

asyncio.run(main())