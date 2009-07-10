import dbus
from object import *
from settings import cSettings

class cConnection(cObject):
    def __init__(self, svc, opath):
        cObject.__init__(self, opath, svc)
        self.ci = dbus.Interface(self.obj, 'org.freedesktop.NetworkManagerSettings.Connection')

    def Dump(self):
       print "Conn:", self.opath
       settings = self.Settings()
       settings.Dump()

       si = dbus.Interface(self.obj, 'org.freedesktop.NetworkManagerSettings.Connection.Secrets')
       security = settings.Security()
       if security != "":
           print " SECRETS:", security
           try:
               # TODO merge them
               secrets = cSettings(si.GetSecrets(security,[],False))
               secrets.Dump()
           except dbus.exceptions.DBusException, e:
               if e.get_dbus_name() == "org.freedesktop.DBus.Error.AccessDenied":
                   print "   Access denied"
               else:
                   print "  ", e
                   print "   FIXME figure out 802-1x secrets"

    def Settings(self):
        return cSettings(self.ci.GetSettings())

