# VRBS Power Control
**V**irtual **R**eality **B**ase **S**tation Power Control

Allows you to toggle the power state of your HTC/Valve Lighthouse Base Stations between *on* and *sleep* modes using Bluetooth LE, on Windows/Linux

Useful if you have an Oculus or other headset that isn't able to automatically manage the power state through SteamVR

## Requirements

- Python >= 3.7 and pip
- Bluetooth >= 4.0 adapter supporting Bluetooth LE (anything made in the last ~10 years should work)
- Windows 10, Linux
  - Linux is not tested yet, and macOS most likely does not work.
- On Windows, you *might* need to pair the base stations to your PC beforehand. In testing this was not necessary, but Windows 10 changed their BLE API and made it less reliable for no good reason.

## Installation

### Windows

- Install python [from the Microsoft Store](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5) 
- Install pip using the following command:
```bash
python -m ensurepip --upgrade
```
- Install bleak using the following command:
```bash
pip install bleak 
```
If the installation of bleak fails on Windows, you might need to upgrade pip, or if that still fails, install the C++ CMake tools [from the Visual Studio Installer](https://visualstudio.microsoft.com/vs/community/)

### Linux

- Install python using your package manager. For example, with Ubuntu:
```bash
sudo apt-get install python3
```
- Install pip using the following command:
```bash
python -m ensurepip --upgrade
```
- Install bleak using the following command:
```bash
pip install bleak
```

## Usage

Run the command with either "on" or "off" as an argument. The default is "on".

For example:

```bash
python vr_bs_control.py on
```

The program will search for any base stations and attempt to send the command to wake/sleep respectively. 

For V1 (HTC) base stations, it can take up to 60 seconds for them to enter sleep mode. Waking up, however, should be almost instant. V2 (Valve) base stations will wake/sleep instantly.

Using the `--save` option will write any found base station's addresses to `basestations.txt`. Upon running the program after this, it will reuse the saved addresses in the text file and skip the *five second long* scan process. Running the program with the `--save` option while saved addresses are already present will re-scan and re-save the addressess, useful if you install a new base station. This file can also easily be manually edited to add or remove addresses if needed.

### Optional Arguments

```bash
htc_bs_control.py [-h] [-s] [-d] [STATE]
```

| Argument | Description |
| --- | --- |
| STATE | Either `on` or `off`, defaults to `on` if not specified |
| -h, --help | Show the help message and exit |
| -s, --save | Saves the addresses of the Base Stations. |
| -d, --dryrun | Runs the program without sending any Bluetooth commands |
