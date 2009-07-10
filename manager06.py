import manager

class cNM_06(manager.cNM):
    def Api(self):
        return "06"

    def SetWifiEnabled(self, v):
        # TODO: async call, catch the state signal and exit
        # weird: synchronous call works, but times out
        # asynchronous call does not work
        self.nmi.setWirelessEnabled(v,
                                    reply_handler=self.quitter_handler,
                                    error_handler=self.quitter_handler)
        global LOOP
        LOOP = True

    def SetOnline(self, v):
        if v:
            self.nmi.wake(True,
                                    reply_handler=self.quitter_handler,
                                    error_handler=self.quitter_handler)
        else:
            self.nmi.sleep(True,
                                    reply_handler=self.quitter_handler,
                                    error_handler=self.quitter_handler)
        global LOOP
        LOOP = True

    def Dump0(self):
        print "State:", self.NM_STATE[self.nmi.state()]
        we = self.nmi.getWirelessEnabled()
        if isinstance(we, tuple):
            print "Wifi enabled:", bool(we[0])
            print "Wifi HW enabled:", bool(we[1])
        else:
            print "Wifi enabled:", bool(we)
        
        try:
            dup = self.nmi.getDialup()
            print "Dialup:", dup
        except dbus.exceptions.DBusException, e:
            #if e.get_dbus_name() == "org.freedesktop.NetworkManager.NoDialup":
            #    pass
            #else:
            print e

    def Devices(self):
        opaths = self.nmi.getDevices()
        return map(cDevice_06, opaths)

    def ActiveConnections(self):
        return []               # at most one active connection, FIXME find it

    def ActivateConnection(self, conn, device, ap):
        # passing *_handler makes the call asynchronous
        self.nmi.setActiveDevice(device.opath, ssid_str(conn.Ssid()),
                                    reply_handler=self.silent_handler,
                                    error_handler=self.err_handler,
                                    )
