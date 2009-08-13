#! /usr/bin/python

import subprocess
import sys
import unittest

import networkmanager.applet.settings as settings

class NoFail(unittest.TestCase):
  def callIt(self, params):
    cmd = sys.path[0] + '/../cnetworkmanager'
    p = subprocess.Popen([cmd, params], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    o = p.communicate()[0]
    # TODO print it if verbose
    if p.returncode != 0:
      raise Exception("Command failed with status", p.returncode, o)

  def testFail(self):
    self.assertRaises(Exception, self.callIt, "--no-such-option")

  def testHelp(self):
    self.callIt("--help")

class SettingsFactory(unittest.TestCase):
  def testWiFi(self):
    ssid = "foo"
    c = settings.WiFi(ssid)

  def testWep(self):
    ssid = "foo"
    c1 = settings.Wep(ssid, "wep_pass")
    c2 = settings.Wep(ssid, "", "ffffffffffffffffffffffffff")

  def testWpa(self):
    ssid = "foo"
    c1 = settings.WpaPsk(ssid, "wep_pass")
    c2 = settings.WpaPsk(ssid, "", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")


if __name__ == '__main__':
    unittest.main()
