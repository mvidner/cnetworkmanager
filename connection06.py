class cConnection_06:
    def __init__(self, applet, id):
        self.id = id
        self.applet = applet

    def Dump(self):
        print "Conn:", self.id

        np = self.applet.ii.getNetworkProperties(self.id, NETWORK_TYPE_ALLOWED)
        ssid = np[0]
        print " ssid:", ssid
        print " time:", dump_time(np[1])
        print " trusted:", bool(np[2])
        print " bssids:", ", ".join(np[3])
        enctype = np[4]
        print " we_cipher:", enctype
        if enctype != 1:
            print " secret:", np[5]
        if enctype == 16:
            print " wep_auth_algorithm:", np[6]
        elif enctype == 0:
            print " wpa_psk_key_mgt:", np[6]
            print " wpa_psk_wpa_version:", np[7]

        return # nm-applet will not tell kfn anyway
        devp = "/org/freedesktop/NetworkManager/Devices/ath0" #FIXME
        netp = devp + "/Networks/" + opath_escape(self.id)
        attempt = 1
        newkey = False
        kfn = self.applet.ii.getKeyForNetwork(devp, netp, ssid, attempt, newkey)
        print " kfn:", kfn
