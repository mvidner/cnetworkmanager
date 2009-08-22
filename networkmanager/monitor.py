"A crude signal monitor for NetworkManager."

import dbus
import dbusclient.monitor
import networkmanager
import device
from base import Bus

class Monitor(dbusclient.monitor.Monitor):
    """A crude signal monitor for NetworkManager.

    It was done before the rest of the library
    and should be replaced with something more fitting the rest.
    """

    def __init__(self):
        super(Monitor, self).__init__(Bus())

        self.watch(
            self.propc_h,
            dbus_interface="org.freedesktop.NetworkManager.Device.Wireless",
            signal_name="PropertiesChanged")
        self.watch(
            self.propc_h,
            dbus_interface="org.freedesktop.NetworkManager.AccessPoint",
            signal_name="PropertiesChanged")

        self.ignore("org.freedesktop.Hal.Device", "PropertyModified")
        self.ignore("fi.epitest.hostap.WPASupplicant.Interface", "ScanResultsAvailable")
        self.ignore("com.redhat.PrinterSpooler", "QueueChanged")
        self.ignore("org.freedesktop.NetworkManager", "StateChange") # deprecated
        self.watch(self.nm_sc_h, "org.freedesktop.NetworkManager", "StateChanged")
        self.watch(self.wpas_isc_h, "fi.epitest.hostap.WPASupplicant.Interface", "StateChange")
        self.watch(self.nmd_sc_h, "org.freedesktop.NetworkManager.Device", "StateChanged")
        self.watch(self.bus_noc_h, "org.freedesktop.DBus", "NameOwnerChanged")

    def bus_noc_h(self, *args, **kwargs):
        (name, old, new) = args
        if new == "":
            new = "gone"
        else:
            new = "at " + new
        print "\tBUS NOC\t%s %s" % (name, new)

    def wpas_isc_h(self, *args, **kwargs):
        opath = kwargs["path"]
        (new, old) = args
        print "\tWPAS %s\t(%s, was %s)" % (new, opath, old.lower())

    def nmd_sc_h(self, *args, **kwargs):
        opath = kwargs["path"]
        (new, old, reason) = args
        news = device.Device.State(new)
        olds = device.Device.State(old)
        reasons = ""
        if reason != 0:
            reasons = " reason %d" % reason
        print "\tDevice State %s\t(%s, was %s%s)" % (news, opath, olds, reasons)

    def nm_sc_h(self, *args, **kwargs):
        s = args[0]
        ss = networkmanager.NetworkManager.State(s)
        print "\tNM State:", ss

    def propc_h(self, *args, **kwargs):
        opath = kwargs["path"]
        props = args[0]
        for k, v in props.iteritems():
            if k == "Strength":
                v = "%u" % v
            line = "\tPROP\t%s\t%s\t(%s)" % (k, v, opath)
            print line
