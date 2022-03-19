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
If the installation of bleak fails on Windows, you might need to install the C++ CMake tools [from the Visual Studio Installer](https://visualstudio.microsoft.com/vs/community/)
### Linux
- Install python using your package manager. For example, with Ubuntu:
```
sudo apt-get install python3
```
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
The program will search for any lighthouse base stations and attempt to send the command to power it on or off respectively. It can take up to 60 seconds for them to enter sleep mode. Powering on, however, should be almost instant.

If you have saved the addresses of your base stations with `--save`, it will use the addresses saved in `basestations.txt` and skip the *five second long* scan process. 

### Optional Arguments
```
htc_bs_control.py [-h] [-s] [-d] [STATE]
```
| Argument | Description | 
| --- | --- |
| STATE | Either `on` or `off`, defaults to `on` if not specified | 
| -h, --help | Show the help message and exit | 
| -s, --save | Saves the addresses of the Base Stations |
| -d, --dryrun | Runs the program without sending any Bluetooth commands |