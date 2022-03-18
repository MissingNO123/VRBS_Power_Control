# HTC BS Control
Control the power state of your HTC/Valve Lighthouse Base Stations using Bluetooth LE

Useful if you have an Oculus or other headset that doesn't let you automatically manage the power state through SteamVR

## Requirements
- Python >= 3.7 and pip
- Bluetooth >= 4.0 adapter supporting Bluetooth LE
- Windows 10, Linux
    - Linux is not tested yet, and macOS probably does not work.
- You *might* need to pair the base stations to your PC beforehand

## Installation
### Windows
- Install python [from the Microsoft Store](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5) 
- Install pip using the following command:
```
python -m ensurepip --upgrade
```
- Install bleak using the following command:
```
pip install bleak 
```

## Usage
Run the command with either "on" or "off" as an argument. The default is "on". 
 
For example: 
```
python htc_bs_control.py on
```
The program will search for any HTC Base stations and attempt to send the command to power it on or off respectively. It can take up to 60 seconds for them to enter sleep mode. Powering on, however, should be almost instant.
