#
# spec file for package cnetworkmanager (Version 0.8)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#



Name:           cnetworkmanager
Version:        0.8.3
Release:        1
Summary:        Command-line client for NetworkManager
License:        GPL v2 or later
Url:            http://vidner.net/martin/software/cnetworkmanager/
Group:          Productivity/Networking/System
BuildRequires:  dbus-1
Requires:       dbus-1-python python-gobject2
Provides:       NetworkManager-client
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Source:         %{name}-%{version}.tar.gz

%description
Cnetworkmanager is a command-line client for NetworkManager, intended
to supplement and replace the GUI applets.



%prep
%setup
#% patch -p1

%build
make

%install
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr sysconfdir=/etc

%check
# nothing

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/cnetworkmanager
/usr/share/cnetworkmanager/cnetworkmanager
/usr/share/cnetworkmanager/pbkdf2.py
/etc/dbus-1/system.d/cnetworkmanager.conf
/etc/dbus-1/system.d/cnetworkmanager-06.conf
%doc /usr/share/doc/packages/cnetworkmanager

%changelog
* Thu Mar 05 2009 mvidner@suse.cz
- v0.8.3
- Fix: secrets leak via o.fd.NMS.Connection.Secrets (CVE-2009-0365)
- Fix: secrets leak via o.fd.NMS.Connection.GetSettings (bnc#479566#c3)
* Sat Nov 22 2008 coolo@suse.de
- buildrequire dbus-1 to fix file list check
* Tue Nov 18 2008 mvidner@suse.cz
- v0.8
- New: --wep-pass
- New: if there is another applet, report its pid
- Fix: do not rely on DBus config from GUI applets
* Fri Nov 07 2008 mvidner@suse.cz
- initial packaging
