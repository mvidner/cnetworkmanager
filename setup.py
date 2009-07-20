#!/usr/bin/env python
# see http://docs.python.org/distutils/

from distutils.core import setup
setup(name = 'cnetworkmanager',
      version = '0.20', # networkmanager.__version__
      description = 'NetworkManager library and CLI',
      author = 'Martin Vidner',
      author_email = 'martin@vidner.net',
      url = 'http://vidner.net/martin/software/cnetworkmanager/',
      license = 'GPL v2 or later',
      #platform = 
      requires = ['dbus'],
      packages = ['networkmanager', 'networkmanager.settings'],
      scripts = ['cnetworkmanager'],
      # data_files = TODO from Makefile
      # classifiers =
      )
