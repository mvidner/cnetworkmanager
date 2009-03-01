PACKAGE=cnetworkmanager
VERSION=0.8

PREFIX=/usr/local
bindir=${PREFIX}/bin
pkgdatadir=${PREFIX}/share/${PACKAGE}
sysconfdir=${PREFIX}/etc
dbusdir=${sysconfdir}/dbus-1/system.d
docdir=${PREFIX}/share/doc/packages/${PACKAGE}

bin_SCRIPTS=cnetworkmanager
pkgdata_DATA=pbkdf2.py
dbus_DATA=cnetworkmanager.conf
doc_DATA=README NEWS COPYING

all:

install:
	install -d ${DESTDIR}${bindir}
	install -t ${DESTDIR}${bindir} ${bin_SCRIPTS}
	install -d ${DESTDIR}${pkgdatadir}
	install -t ${DESTDIR}${pkgdatadir} -m644 ${pkgdata_DATA}
	install -d ${DESTDIR}${dbusdir}
	install -t ${DESTDIR}${dbusdir} -m644 ${dbus_DATA}
	install -d ${DESTDIR}${docdir}
	install -t ${DESTDIR}${docdir} -m644 ${doc_DATA}

dist:
	mkdir -p ${PACKAGE}-${VERSION}
	cp -t ${PACKAGE}-${VERSION} ${PACKAGE}.spec Makefile ${bin_SCRIPTS} ${pkgdata_DATA} ${dbus_DATA} ${doc_DATA}
	tar cvfz ${PACKAGE}-${VERSION}.tar.gz ${PACKAGE}-${VERSION}

# bikemake: serves similar purpose as automake, but is much less resource hungry
