import asyncio
import time
from bleak import BleakScanner, BleakClient
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

basestations = []

async def powerState(bs, value):
    cmd = CMD_ON if value else CMD_OFF
    async with BleakClient(bs) as client:
        print("Connecting to ...  %s..." % bs.name)
        while client.is_connected is False:
            time.sleep(0.05)
        print("Connected!    ...  %s!" % bs.name)
        p = await client.write_gatt_char(v1_Power_Char, cmd)
        print("Powering %s  ...  %s " % ("ON " if PowerState is True else "OFF", bs.name))
        return await client.disconnect()

async def main():
    print("Scanning...")
    devices = await BleakScanner.discover()
    if len(devices) <= 1:
        print("No devices found.")
        quit()
    for d in devices:
        if d.name is not None and d.name.startswith('HTC BS '):
            print("Found Base Station: %s" % d.name)
            basestations.append(d) 
    for bs in basestations:
        await powerState(bs, PowerState)
        print("")

asyncio.run(main())