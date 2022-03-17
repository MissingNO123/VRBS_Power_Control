# HTC BS Control
Control the power state of your HTC Vive Base Stations (v1 only for now) using Bluetooth LE
 
Currently, the program only works with the first generation HTC Vive Base Stations (the square ones), not the newer second generation ones from Valve (yet). This is beacause I do not own any to test with.

## Requirements
- Python >= 3.7 and pip
- Bluetooth >= 4.0 adapter supporting Bluetooth LE
- Windows 10, Linux
    - Linux is not tested yet, and macOS probably does not work.
- C++ CMake tools 
- The base stations have been paired to your PC through Bluetooth settings.
    - If you skip this, Windows will try to ask if you want to pair while the program is running. This will cause the program to stall out.

## Installation
- If you are on Windows, install the C++ CMake tools from the Visual Studio Installer
- Install bleak using the following command:
```bash
pip install bleak 
```

 
## Usage
Run the command with either "on" or "off" as an argument. The default is "on". 
 
For example: 
```bash
python htc_bs_control.py on
```
The program will search for any HTC Base stations and attempt to send the command to power it on or off respectively. It can take up to 60 seconds for them to power down. Powering on, however, should be almost instant.
