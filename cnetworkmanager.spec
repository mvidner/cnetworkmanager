Name:           cnetworkmanager
Version:        0.8
Release:        1
Summary:        Command-line client for NetworkManager
License:        GPL
URL:		http://vidner.net/martin/software/cnetworkmanager/
Group:          Productivity/Networking/System
Requires:	dbus-1-python python-gobject2
BuildRoot:      %{_tmppath}/%{name}-root
BuildArch:	noarch
Source:		%{name}-%{version}.tar.gz

%description

Cnetworkmanager is a command-line client for NetworkManager,
intended to supplement and replace the GUI applets.

Authors:
--------
    Martin Vidner <mvidner@suse.cz>

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
/etc/dbus-1/system.d/cnetworkmanager.conf
/etc/dbus-1/system.d/cnetworkmanager-06.conf
%doc /usr/share/doc/packages/cnetworkmanager

%changelog

* Fri Nov 07 2008 - Martin Vidner <mvidner@suse.cz>
- Initial packaging
