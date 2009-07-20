#! /usr/bin/python

import subprocess
import sys
import unittest

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

if __name__ == '__main__':
    unittest.main()
