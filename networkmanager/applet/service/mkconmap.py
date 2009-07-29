import hashlib
import dbus
import uuid
import math
from binascii import hexlify

import pbkdf2

def mkconmap_wifi(ssid):
    return {
        'connection': {
            'id': '_cnm_handcrafted_',
            'uuid': str(uuid.uuid1()), # new in oS 11.1
            'type': '802-11-wireless',
            },
        '802-11-wireless': {
            'ssid': dbus.ByteArray(ssid),
            'mode': 'infrastructure',
            },
        }

def _elongate(s, tlen):
    "repeat string s to target length tlen"
    if s == "":
        return ""
    copies_needed = int(math.ceil(tlen / float(len(s))))
    return (s * copies_needed)[:tlen]

# http://www.mail-archive.com/networkmanager-list@gnome.org/msg07935.html
def _wep_passphrase_to_hash(p):
    return hashlib.md5(_elongate(p, 64)).hexdigest()

def mkconmap_wep_pass(ssid, key):
    cm = mkconmap_wifi(ssid)
    cm["802-11-wireless"]["security"] = "802-11-wireless-security"
    cm["802-11-wireless-security"] = {}
    cm["802-11-wireless-security"]["key-mgmt"] = "none"
    cm["802-11-wireless-security"]["wep-tx-keyidx"] = 0
    cm["802-11-wireless-security"]["wep-key0"] = _wep_passphrase_to_hash(key)
    return cm

def mkconmap_wep(ssid, key):
    cm = mkconmap_wifi(ssid)
    cm["802-11-wireless"]["security"] = "802-11-wireless-security"
    cm["802-11-wireless-security"] = {}
    cm["802-11-wireless-security"]["key-mgmt"] = "none"
    cm["802-11-wireless-security"]["wep-tx-keyidx"] = 0
    cm["802-11-wireless-security"]["wep-key0"] = key
    return cm

def mkconmap_psk(ssid, key):
    cm = mkconmap_wifi(ssid)
    cm["802-11-wireless"]["security"] = "802-11-wireless-security"
    cm["802-11-wireless-security"] = {}
    cm["802-11-wireless-security"]["key-mgmt"] = "wpa-psk"
    cm["802-11-wireless-security"]["psk"] = hexlify(pbkdf2.pbkdf2(key, ssid, 4096, 32))
    cm["802-11-wireless-security"]["group"] =    ["tkip", "ccmp"]
    cm["802-11-wireless-security"]["pairwise"] = ["tkip", "ccmp"]
    return cm


