import readline
import shlex

import fastkml


DEFAULT_KML = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <Style id="red">
            <IconStyle>
                <Icon>
                    <href>http://maps.google.com/mapfiles/ms/icons/red-dot.png</href>
                </Icon>
            </IconStyle>
        </Style>
        <Style id="yellow">
            <IconStyle>
                <Icon>
                    <href>http://maps.google.com/mapfiles/ms/icons/yellow-dot.png</href>
                </Icon>
            </IconStyle>
        </Style>
        <Style id="green">
            <IconStyle>
                <Icon>
                    <href>http://maps.google.com/mapfiles/ms/icons/green-dot.png</href>
                </Icon>
            </IconStyle>
        </Style>
    </Document>
</kml>
""".encode("utf-8")


class Shell:
    def __init__(self, wifis):
        self.wifi_networks = wifis
        self.current_list = []

        for w in self.wifi_networks:
            self.current_list.append(w)
        
        self.commands = {
            "help": {
                "description": ["Usage: help [command]",
                                " Prints all available commands or the help for a specific command"],
                "execute": self.help
            },
            "show": {
                "description": ["Usage: show [number [number ...]]",
                                "  Show all WiFi networks or specific ones"],
                "execute": self.show
            },
            "reset": {
                "description": ["Usage: reset"
                                "  Reinitializes all filters"],
                "execute": self.reset
            },
            "keep": {
                "description": ["Usage: keep security_type [security_type...]",
                                "  Keeps only networks matching certain security types"],
                "execute": self.keep
            },
            "rm": {
                "description": ["Usage: rm security_type [security_type...]",
                                "  Deletes all networks matching certain security types"],
                "execute": self.rm
            },
            "keepname": {
                "description": ["Usage: keepname name [name ...]",
                                "  Keeps only networks with the given SSID(s)"],
                "execute": self.keepname
            },
            "rmname": {
                "description": ["Usage: rmname name [name ...]",
                                "  Removes all networks with the given SSID(s)"],
                "execute": self.rmname
            },
            "dump": {
                "description": ["Usage: dump filename",
                                  "Dumps the current list of networks in a KML file"],
                "execute": self.dump
            },
            "dedup": {
                "description": ["Usage: dedup",
                                "  Removes all duplicate WiFi networks"],
                "execute": self.dedup
            }
        }  

    def run(self):
        while True:
            command = input(self._get_prompt()).strip()
            parts = shlex.split(command)

            command = parts[0]

            if len(parts) > 1:
                args = parts[1:]
            else:
                args = []

            if command == "quit" or command == "exit" or not command:
                return 
            elif command in self.commands.keys():
                return_code = self.commands[command]["execute"](args)
                if return_code == 3:
                    self._usage(command)
                elif return_code != 0:
                    print(command, "returned non-zero error code", return_code)
            else:
                print("Error: command \"{}\" not found".format(command))

    def show(self, args):
        if len(args) == 0:
            for w in self.current_list:
                print(w)
        else:
            for idx in args:
                try:
                    idx = int(idx)
                    w = self.current_list[idx]
                    print(w)
                except ValueError:
                    print("Error:", idx, "is not a number")
                except IndexError:
                    print("WiFi network no.", idx, "does not exist")
        return 0
    
    def reset(self, args):
        if len(args) != 0:
            return 3

        self.current_list = []
        for w in self.wifi_networks:
            self.current_list.append(w)
        return 0
    
    def keep(self, args):
        if len(args) == 0:
            return 3
        
        new_list = []
        for w in self.current_list:
            has_any_cap = False
            for cap in args:
                if w.has_cap(cap):
                    has_any_cap = True
                    break
            if has_any_cap:
                new_list.append(w)
        self.current_list = new_list
        return 0

    def rm(self, args):
        if len(args) == 0:
            return 3
        
        new_list = []
        for w in self.current_list:
            has_any_cap = False
            for cap in args:
                if w.has_cap(cap):
                    has_any_cap = True
                    break
            if not has_any_cap:
                new_list.append(w)
        self.current_list = new_list
        return 0

    def keepname(self, args):
        if len(args) == 0:
            return 3

        new_list = []
        for w in self.current_list:
            if w.ssid in args:
                new_list.append(w)
        self.current_list = new_list
        return 0

    def rmname(self, args):
        if len(args) == 0:
            return 3
        
        new_list = []
        for w in self.current_list:
            if w.ssid not in args:
                new_list.append(w)
        self.current_list = new_list
        return 0

    def dump(self, args):
        if len(args) != 1:
            return 3

        k = fastkml.KML()
        k.from_string(DEFAULT_KML)

        document = list(k.features())[0]
        for w in self.current_list:
            document.append(w.placemark)
        
        with open(args[0], "w") as f:
            f.write(k.to_string())
        return 0

    def dedup(self, args):
        if len(args) != 0:
            return 3

        new_list = []
        for w in self.current_list:
            if w not in new_list:
                new_list.append(w)
        self.current_list = new_list
        return 0
    
    def help(self, args):
        if len(args) == 0:
            print("Commands:", ' '.join(self.commands.keys()))
            print("You can also use \"help <command>\"")
        else:
            self._usage(args[0])
        return 0

    def _usage(self, command):
        if command == "quit" or command == "exit":
            print("Usage: [quit, exit]")
            print("  Exits the program.")
        elif command in self.commands.keys():
            print('\n'.join(self.commands[command]["description"]))
        else:
            print("No such command:", command)

    def _get_prompt(self):
        return str(len(self.current_list)) + " >> "