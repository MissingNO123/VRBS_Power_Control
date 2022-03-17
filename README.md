# HTC-BS-Control
 Control power state of HTC Vive Base Stations (v1 only for now) using Bluetooth LE

 # Requirements
 - Python >= 3.7 and pip
 - Bluetooth >= 4.0 adapter supporting Bluetooth LE
 - Windows 10, Linux
    - Linux is not tested yet, and macOS probably does not work.
 - C++ CMake tools 

 # Installation
 - If you are on Windows, install the C++ CMake tools from the Visual Studio Installer
 - Install bleak using the following command:
 ```pip install bleak```

 # Usage
 Run the command with either "on" or "off" as an argument. The default is "on". 
 
 For example: 
 ```
 python htc_bs_control.py on
 ```
 The program will search for any HTC Base stations and attempt to send the command to power it on or off respectively. It can take up to 60 seconds for them to power down. Powering on should be almost instant, however.

 Currently, the program only works with the first generation HTC Vive Base Stations (the square ones), not the newer second generation ones from Valve (yet). This is beacause I do not own any to test with.
