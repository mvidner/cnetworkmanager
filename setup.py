#!/usr/bin/env python
# see http://docs.python.org/distutils/

from distutils.core import setup
setup(name = 'cnetworkmanager',
      version = '0.21.1',
      description = 'NetworkManager library and CLI',
      author = 'Martin Vidner',
      author_email = 'martin@vidner.net',
      url = 'http://vidner.net/martin/software/cnetworkmanager/',
      license = 'GPL v2 or later',
      #platform = 
      requires = ['dbus'],
      packages = ['networkmanager',
                  'networkmanager.applet',
                  'networkmanager.applet.service',
                  'dbusclient'],
      scripts = ['cnetworkmanager'], # -server is not ready yet
      data_files = [
        ('/etc/dbus-1/system.d', ['cnetworkmanager.conf']),
        ]
      # classifiers =
      )
