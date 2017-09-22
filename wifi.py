import re


class MobileNetworkError(BaseException):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg


class WiFi:
    def __init__(self, placemark):
        self.ssid = placemark.name
        self.description = placemark.description
        self.coordinates = placemark.geometry
        self.placemark = placemark

        self._read_description()

    def _read_description(self):
        regex = re.compile(r'^BSSID: <b>(?P<bssid>[a-z0-9]{2}:[a-z0-9]{2}:[a-z0-9]{2}:[a-z0-9]{2}:[a-z0-9]{2}:[a-z0-9]{2})</b><br/>Capabilities: <b>(?P<capabilities>.*)</b><br/>Frequency: <b>(?P<frequency>[0-9]+)</b><br/>Timestamp: <b>(?P<timestamp>[0-9]+)</b><br/>Date: <b>(?P<date>.*)</b>')
        results = regex.search(self.description)
        
        if not results:
            raise MobileNetworkError("Network " + self.ssid + " is a mobile network")

        self.bssid = results.group("bssid")
        caps = results.group("capabilities")
        self.frequency = results.group("frequency")
        self.timestamp = results.group("timestamp")
        self.date = results.group("date")

        self.capabilities = []
        caps = caps.split("[")
        for cap in caps:
            cap = cap.strip("]").strip()
            if cap:
                self.capabilities.append(cap)

    def has_cap(self, cap):
        if cap in self.capabilities:
            return True

        for mycap in self.capabilities:
            if mycap.lower() == cap.lower():
                return True
        
        if cap.lower() == "open":
            if len(self.capabilities) == 1 and self.capabilities[0] == "ESS":
                return True
        
        # Classic WPA2
        if cap.lower() == "wpa2" or cap.lower() == "wpa2-psk":
            if "WPA2-PSK-CCMP+TKIP" in self.capabilities or \
               "WPA2-PSK-CCMP" in self.capabilities or \
               "WPA2-PSK-TKIP" in self.capabilities or \
               "WPA2-PSK-TKIP+CCMP" in self.capabilities:
                return True

        # Classic WPA
        if cap.lower() == "wpa" or cap.lower() == "wpa-psk":
            if "WPA-PSK-TKIP" in self.capabilities or \
               "WPA-PSK-CCMP+TKIP" in self.capabilities or \
               "WPA-PSK-CCMP" in self.capabilities or \
               "WPA-PSK-TKIP+CCMP" in self.capabilities:
                return True
        
        # WPA-EAP (Enterprise)
        if cap.lower() == "wpa-eap":
            if "WPA-EAP-CCMP" in self.capabilities:
                return True

        # WPA2-EAP (Enterprise)
        if cap.lower() == "wpa2-eap":
            if "WPA2-EAP-CCMP+TKIP" in self.capabilities or \
               "WPA2-EAP-CCMP" in self.capabilities or \
               "WPA2-EAP+FT/EAP-CCMP" in self.capabilities or \
               "WPA2-EAP-TKIP+CCMP" in self.capabilities:
                return True
        
        return False

    def __str__(self):
        s = "["+ self.ssid +"] "+ self.bssid +"\t"
        s += "(" + str(self.coordinates.y) + " ; " + str(self.coordinates.x) + ")\n"
        for cap in self.capabilities:
            s += "\t" + cap
            s += "\n"
        return s

    def __eq__(self, other):
        return self.bssid == other.bssid