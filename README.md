# TankPy -- A WarDriving ToolKit

## Description

This project provides a shell to work with KML files outputed by the WiGLE WiFi Android app.

It makes it easy to filter networks depending on their name, their protection etc.

## Installation

### Dependencies

- `fastkml`
- `readline`

### Installing

- Clone this repository
- Run `./tankpy.py YourWiGLEdump.kml`
- Once in the shell, use the `help` command or check out the brief documentation just below

## Documentation

*I know the code isn't all that pretty, it was a quick-and-dirty project*

- Use `keep` or `rm` to respectively only keep or remove all networks with the given protection. For now, the script recognizes either the exact protection type (e.g. WPA2-EAP-TKIP+CCMP) or some shortcuts like `open`, `wpa`, `wpa2`, `wep`, `wpa-eap`, `wpa2-eap`
- Use `keepname` or `rmname` to filter networks based on their SSID
- Use `show` to show all current networks or `show n` to show the *n*-th network (it includes its SSID, BSSID, location and capabilities)
- If you are using multiple overlapping KML files, use `dedup` to remove duplicate access points (based on their BSSID)
- The `dump` command allows you to dump the current stations to a KML file to view it in an external program
- Finally, use `reset` to clear all the filters