import dbus
from svc_connection import Connection
from settings import cSettings, NM_AUTH_TYPE_NONE
from util import *

class Connection_06(Connection):
    def __init__(self, opath, conmap):
        bus = dbus.SystemBus()
        dbus.service.Object.__init__(self, bus, opath)
        #print "C6", conmap
        self.settings = cSettings(conmap)

    # dbus.service.method
    def getNetworkProperties(self):
        # essid, timestamp, ?, bssids, we_cipher, ?, ...
        # we_cipher=16: i wep_auth_algorithm
        # we_cipher=0:  i wpa_psk_key_mgt, i wpa_psk_wpa_version
        ssid = ssid_str(self.settings.Ssid())
        time = self.settings.Timestamp() # last sucessfully connected? seen?
        trusted = self.settings.Trusted()
        bssids = dbus.Array(self.settings.SeenBssids(), signature="s")
        r = [ssid, time, trusted, bssids]
        security = self.getKeyForNetwork("fake key")
        r.extend(security)
        return tuple(r)

    # dbus.service.method
    def getKeyForNetwork(self, fake="no"):
        if fake == "no":
            key = self.settings.Key()
        else:
            key = ""

        # security
        cip = self.settings.WeCipher()
        if cip == NM_AUTH_TYPE_NONE:
            security = tuple([cip])
        elif cip == NM_AUTH_TYPE_WEP40 or cip == NM_AUTH_TYPE_WEP104:
            wep_auth_algorithm = self.settings.WepAuthAlgorithm()
            security = (cip, key, wep_auth_algorithm)
        elif cip == NM_AUTH_TYPE_WPA_PSK_AUTO or cip == NM_AUTH_TYPE_TKIP or \
                cip == NM_AUTH_TYPE_CCMP:
            wpa_psk_key_mgt = self.settings.PskKeyMgt()
            wpa_psk_wpa_version = self.settings.PskWpaVersion()
            security = (cip, key, wpa_psk_key_mgt, wpa_psk_wpa_version)
        elif cip == NM_AUTH_TYPE_WPA_EAP:
            security = tuple([cip]) # TODO more...
        elif cip == NM_AUTH_TYPE_LEAP:
            security = tuple([cip]) # TODO more...
        return security
