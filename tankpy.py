#!/usr/bin/env python3

import sys
import code
from wifi import WiFi, MobileNetworkError
from shell import Shell

import fastkml

def load_kml_file(filename):
    k = fastkml.KML()

    file_contents = open(filename, "r").read().encode("utf-8")
    k.from_string(file_contents)

    document = list(k.features())[0]
    folder = list(document.features())[0]

    wifis_raw = list(folder.features())

    wifis = []
    for w in wifis_raw:
        try:
            n = WiFi(w)
            wifis.append(n)
        except MobileNetworkError:
            pass
    return wifis


def main():
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "kml_file [kml_file ...]")
        sys.exit(3)
    
    wifis = []
    for i in range(1, len(sys.argv)):
        ws = load_kml_file(sys.argv[i])
        wifis += ws
    
    print("Loaded", len(wifis), "WiFi networks")
    shell = Shell(wifis)
    shell.run()


if __name__ == "__main__":
    main()