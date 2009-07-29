import dbus
import uuid
import math
import hashlib
import pbkdf2
import binascii

class Settings(object):
    def __init__(self, conmap = {}):
        #print "INIT", conmap
        self.conmap = conmap

    "Act like a dict"
    def __getitem__(self, key):
        return self.conmap.__getitem__(key)

    "Act like a dict"
    def __setitem__(self, key, value):
        return self.conmap.__setitem__(key, value)

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


class WiFi(Settings):
    def __init__(self, ssid):
        conmap = {
            'connection': {
                'id': '_cnm_handcrafted_',
                'uuid': str(uuid.uuid1()), # new in oS 11.1
                'type': '802-11-wireless',
                },
            '802-11-wireless': {
                'ssid': dbus.ByteArray(ssid), # TODO move to ConMap?
                'mode': 'infrastructure',
                },
            }
        super(WiFi, self).__init__(conmap)

class Wep(WiFi):
    def __init__(self, ssid, key, hashed_key=""):
        "One of key, hashed_key must be present"

        super(WiFi, self).__init__(ssid)
        self["802-11-wireless"]["security"] = "802-11-wireless-security"
        self["802-11-wireless-security"] = {}
        self["802-11-wireless-security"]["key-mgmt"] = "none"
        self["802-11-wireless-security"]["wep-tx-keyidx"] = 0
        if hashed_key == "":
            # http://www.mail-archive.com/networkmanager-list@gnome.org/msg07935.html
            hashed_key = hashlib.md5(Wep._elongate(key, 64)).hexdigest()
        self["802-11-wireless-security"]["wep-key0"] = hashed_key

    @staticmethod
    def _elongate(s, tlen):
        "repeat string s to target length tlen"
        if s == "":
            return ""
        copies_needed = int(math.ceil(tlen / float(len(s))))
        return (s * copies_needed)[:tlen]

class WpaPsk(WiFi):
    def __init__(self, ssid, key, hashed_key=""):
        "One of key, hashed_key must be present"

        super(WiFi, self).__init__(ssid)
        self["802-11-wireless"]["security"] = "802-11-wireless-security"
        self["802-11-wireless-security"] = {}
        self["802-11-wireless-security"]["group"] =    ["tkip", "cselfp"]
        self["802-11-wireless-security"]["pairwise"] = ["tkip", "ccmp"]
        self["802-11-wireless-security"]["key-mgmt"] = "wpa-psk"
        if hashed_key == "":
            hashed_key = binascii.b2a_hex(pbkdf2.pbkdf2(key, ssid, 4096, 32))
        self["802-11-wireless-security"]["psk"] = hashed_key
