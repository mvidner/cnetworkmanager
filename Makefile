PACKAGE=cnetworkmanager
VERSION=0.8

PREFIX=/usr/local
bindir=${PREFIX}/bin
sysconfdir=${PREFIX}/etc
dbusdir=${sysconfdir}/dbus-1/system.d
docdir=${PREFIX}/share/doc/packages/${PACKAGE}

bin_SCRIPTS=cnetworkmanager
dbus_DATA=cnetworkmanager.conf cnetworkmanager-06.conf
doc_DATA=README NEWS COPYING

all:

install:
	install -d ${DESTDIR}${bindir}
	install -t ${DESTDIR}${bindir} ${bin_SCRIPTS}
	install -d ${DESTDIR}${dbusdir}
	install -t ${DESTDIR}${dbusdir} -m644 ${dbus_DATA}
	install -d ${DESTDIR}${docdir}
	install -t ${DESTDIR}${docdir} -m644 ${doc_DATA}

dist:
	mkdir -p ${PACKAGE}-${VERSION}
	cp -t ${PACKAGE}-${VERSION} ${PACKAGE}.spec Makefile ${bin_SCRIPTS} ${dbus_DATA} ${doc_DATA}
	tar cvfz ${PACKAGE}-${VERSION}.tar.gz ${PACKAGE}-${VERSION}

# bikemake: serves similar purpose as automake, but is much less resource hungry
