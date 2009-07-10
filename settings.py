# 06
NM_AUTH_TYPE_WPA_PSK_AUTO = 0x00000000
NM_AUTH_TYPE_NONE         = 0x00000001
NM_AUTH_TYPE_WEP40        = 0x00000002
NM_AUTH_TYPE_WPA_PSK_TKIP = 0x00000004
NM_AUTH_TYPE_WPA_PSK_CCMP = 0x00000008
NM_AUTH_TYPE_WEP104       = 0x00000010
NM_AUTH_TYPE_WPA_EAP      = 0x00000020
NM_AUTH_TYPE_LEAP         = 0x00000040

IW_AUTH_ALG_OPEN_SYSTEM   = 0x00000001
IW_AUTH_ALG_SHARED_KEY    = 0x00000002
IW_AUTH_ALG_LEAP          = 0x00000004

class cSettings:
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

    def Timestamp(self):
        try:
            return self.conmap["connection"]["timestamp"]
        except KeyError:
            return 0

    def Trusted(self):
        # false by default
        return False

    def SeenBssids(self):
        try:
            return self.conmap["802-11-wireless"]["seen-bssids"]
        except KeyError:
            return []

    # for 06
    def WeCipher(self):
        k = self.Key()
        if len(k) == 26:
            return NM_AUTH_TYPE_WEP104
        elif len(k) == 64:
            return NM_AUTH_TYPE_WPA_PSK_AUTO
        elif len(k) == 0:
            return NM_AUTH_TYPE_NONE
        print "Defaulting cipher type to none"
        return NM_AUTH_TYPE_NONE

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

    def WepAuthAlgorithm(self):
        print "FIXME Defaulting WEP auth alg to open"
        return IW_AUTH_ALG_OPEN_SYSTEM

    def PskKeyMgt(self):
        print "FIXME Defaulting PSK key mgmt to 2"
        return 2

    def PskWpaVersion(self):
        print "FIXME Defaulting WPA version to 2"
        return 2

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

