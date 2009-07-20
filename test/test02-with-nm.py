#! /usr/bin/python

import subprocess
import sys
import unittest

class WithNM(unittest.TestCase):
  def callIt(self, params):
    cmd = sys.path[0] + '/../cnetworkmanager'
    p = subprocess.Popen([cmd, params], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    o = p.communicate()[0]
    # TODO print it if verbose
    if p.returncode != 0:
      raise Exception("Command failed with status", p.returncode, o)

  def testDev(self):
    self.callIt("--dev")

  def testActCon(self):
    self.callIt("--actcon")

  def testUsrCon(self):
    self.callIt("--usrcon")

  def testSysCon(self):
    self.callIt("--syscon")

  def testAP(self):
    self.callIt("--ap")

  def testNets(self):
    self.callIt("--nets")

if __name__ == '__main__':
    unittest.main()
