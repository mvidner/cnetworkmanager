"""A library for NetworkManager

User's view: the computer has an IP address and can connect to one of the
WiFi networks around, or to a wire.

Admin's view: the computer has network interfaces (on network devices),
which have configurations (/etc/network...). They can connect to access
points around. A connected interface has an IP config.

NetworkManager's view: computer has L{Devices<Device>}, some of which are
managed by L{NetworkManager}.  WiFi devices see L{APs<AccessPoint>}. There are
L{Connections<networkmanager.applet.Connection>} which specify how a type of
device (wired, wireless) can be activated. The connections are provided by two
services separate from NM: NMSS and NMUS.  To connect, the needed ingredients
are a Connection (+its service), a Device, optionally an L{AccessPoint}. It
results in an L{ActiveConnection} which remembers its ingredients. The device
then knows its L{IP4Config} and L{DHCP4Config}.

(TODO: explain VPN plugins, modems (ModemManager))

For details, see

  - U{http://projects.gnome.org/NetworkManager/developers/spec.html}
  - U{http://live.gnome.org/NetworkManagerConfigurationSpecification}
"""
#__docformat__ = "restructuredtext en"
# TODO hyperlinks to classes in epydoc. a diagram?
from accesspoint import AccessPoint
from activeconnection import ActiveConnection
from device import Device, IP4Config, DHCP4Config
from networkmanager import NetworkManager

__all__ = ["AccessPoint", "ActiveConnection", "Device",
           "DHCP4Config", "IP4Config", "NetworkManager", ]
