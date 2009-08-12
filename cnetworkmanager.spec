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
Version:        0.21
Release:        1
Summary:        Command-line client for NetworkManager
License:        GPL v2 or later
Url:            http://vidner.net/martin/software/cnetworkmanager/
Group:          Productivity/Networking/System
# build time reqs same as run time because we run tests
BuildRequires:  dbus-1-python python-gobject2
%if 0%{?suse_version} <= 1100 
BuildRequires:  python-devel
%endif
# if suse>11.1 or not suse:
%if %{?suse_version: %{suse_version} > 1110} %{!?suse_version:1}
BuildArch:      noarch
%endif
Requires:       dbus-1-python python-gobject2
Requires:	NetworkManager >= 0.7.0
Provides:       NetworkManager-client
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         %{name}-%{version}.tar.gz
%{py_requires}

%description
Cnetworkmanager is a command-line client for NetworkManager, intended
to supplement and replace the GUI applets.



%prep
%setup
#% patch -p1

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT --record-rpm=INSTALLED_FILES
# mark the /etc files as config
sed -i 's,^/etc,%config /etc,' INSTALLED_FILES

%check
make check-nonm

%clean
rm -rf %{buildroot}

%files -f  INSTALLED_FILES
%defattr(-,root,root)
%doc README COPYING HACKING NEWS screenshots.html
%changelog
