class Settings:
    def __init__(self, conmap):
        #print "INIT", conmap
        self.conmap = conmap

    def Type(self):
        return self.conmap["connection"]["type"]

    def ID(self):
        return self.conmap["connection"]["id"]

    def Ssid(self):
        try:
            return self.conmap["802-11-wireless"]["ssid"]
        except KeyError:
            pass
        # probably 802-3-ethernet
        return ""

    def Key(self):
        try:
            return self.conmap["802-11-wireless-security"]["psk"]
        except KeyError:
            pass
        try:
            return self.conmap["802-11-wireless-security"]["wep-key0"]
        except KeyError:
            pass
        # no key
        return ""

    def Security(self):
        try:
            return self.conmap[self.Type()]["security"]
        except KeyError:
            return ""

    def isNet(self, net_name):
        return self.ID() == net_name or self.Ssid() == net_name

    # FIXME check spec/NM what to censor
    secrets = dict.fromkeys(["wep-key0", "psk"])

    def ConMap(self):
        "For GetSettings: censor secrets."

        cm = dict()
        for n1, v1 in self.conmap.iteritems():
            cm[n1] = dict()
            for n2, v2 in v1.iteritems():
                cv2 = v2
                if self.secrets.has_key(n2):
                    cv2 = ""
                cm[n1][n2] = cv2
        return cm

    def SecMap(self):
        "For GetSecrets: only secrets."
        s = self.Security()
        r = {
            s: self.conmap[s]
            }
        print "SECMAP", r
        return r

    def Dump(self):
        for n1, v1 in self.conmap.iteritems():
            print " ",n1
            for n2, v2 in v1.iteritems():        
                print "   %s: %s" % (n2, v2)

