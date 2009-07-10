import dbus
import time
import object

NMI = 'org.freedesktop.NetworkManager'

class cNM(object.cObject):
    # TODO: pull them from introspection.xml
    NM_STATE = ["UNKNOWN", "ASLEEP", "CONNECTING", "CONNECTED", "DISCONNECTED",]

    def __init__(self, opath, options):
        object.cObject.__init__(self, opath)
        self.nmi = dbus.Interface(self.obj, NMI)
        self.options = options

    def get_property(self, property_name):
        return object.cObject.get_property(self, NMI, property_name)

    def set_property(self, property_name, value):
        return object.cObject.set_property(self, NMI, property_name, value)

    def Api(self):
        return "common"

    def Dump0(self):
        "Dumps its own info (not owned objects)."
        pass

    def Dump(self):
        self.Dump0()
        if self.options.dev:
            for device in self.Devices():
                device.Dump()

        if self.options.actcon:
            print "Active Connections"
            aconns = self.ActiveConnections()
            for aconn in aconns:
                aconn.Dump()

    def ListNets(self):
        print "Wifi Networks:"
        for dev in self.Devices():
            dev.ListNets()

    def err_handler(self, *args):
        print "ERR:", args

    def silent_handler(self, *args):
        pass
        #print "BOO!:", args

    def quitter_handler(self, *args):
        # exit the loop that runs only because of us
        print "padla"
        sys.exit(0)

    def WatchState(self):
        self.bus.add_signal_receiver(self.state_changed_handler,
                                dbus_interface=NMI,
                                signal_name="StateChanged")

    def state_changed_handler(self, *args):
        s = args[0]
        ss = self.NM_STATE[s]
        print time.strftime("(%X)"),
        print "State:", ss
