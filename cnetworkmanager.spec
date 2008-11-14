Name:           cnetworkmanager
Version:        0.7.1
Release:        1
Summary:        Command-line client for NetworkManager
License:        GPL
URL:		http://vidner.net/martin/software/cnetworkmanager/
Group:          Productivity/Networking/System
Requires:	dbus-1-python python-gobject2
BuildRoot:      %{_tmppath}/%{name}-root
BuildArch:	noarch
Source:		cnetworkmanager
Source1:	COPYING
Source2:	README

%description

Cnetworkmanager is a command-line client for NetworkManager,
intended to supplement and replace the GUI applets.

Authors:
--------
    Martin Vidner <mvidner@suse.cz>

%prep
#%setup -n %{name}
#% patch -p1
cp %SOURCE1 %SOURCE2 .

%build

# nothing

%install
install -d $RPM_BUILD_ROOT/%_bindir
install -t $RPM_BUILD_ROOT/%_bindir %SOURCE0

%check

# nothing

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%_bindir/cnetworkmanager
%doc COPYING README

%changelog

* Fri Nov 07 2008 - Martin Vidner <mvidner@suse.cz>
- Initial packaging
