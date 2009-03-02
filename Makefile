PACKAGE=cnetworkmanager
VERSION=0.8

PREFIX=/usr/local
bindir=${PREFIX}/bin
pkgdatadir=${PREFIX}/share/${PACKAGE}
sysconfdir=${PREFIX}/etc
dbusdir=${sysconfdir}/dbus-1/system.d
docdir=${PREFIX}/share/doc/packages/${PACKAGE}

nodist_bin_SCRIPTS=cnetworkmanager-proxy
pkgdata_SCRIPTS=cnetworkmanager
pkgdata_DATA=pbkdf2.py
dbus_DATA=cnetworkmanager.conf
doc_DATA=README NEWS COPYING
EXTRA_DIST=cnetworkmanager-proxy.in

all:
	for IN in cnetworkmanager-proxy.in; do \
	    OUT=$${IN%.in}; \
	    sed \
		-e "s|@configure_input@|$$OUT. Generated from $$IN by bikemake.|g" \
		-e 's|@PREFIX@|${PREFIX}|g' \
		-e 's|@PACKAGE@|${PACKAGE}|g' \
		<$$IN >$$OUT ;\
	done

install:
	install -d ${DESTDIR}${bindir}
	install -T cnetworkmanager-proxy ${DESTDIR}${bindir}/cnetworkmanager
	install -d ${DESTDIR}${pkgdatadir}
	install -t ${DESTDIR}${pkgdatadir} ${pkgdata_SCRIPTS}
	install -d ${DESTDIR}${pkgdatadir}
	install -t ${DESTDIR}${pkgdatadir} -m644 ${pkgdata_DATA}
	install -d ${DESTDIR}${dbusdir}
	install -t ${DESTDIR}${dbusdir} -m644 ${dbus_DATA}
	install -d ${DESTDIR}${docdir}
	install -t ${DESTDIR}${docdir} -m644 ${doc_DATA}

dist:
	rm -rf ${PACKAGE}-${VERSION}
	mkdir -p ${PACKAGE}-${VERSION}
	cp -t ${PACKAGE}-${VERSION} ${PACKAGE}.spec Makefile ${pkgdata_SCRIPTS} ${pkgdata_DATA} ${dbus_DATA} ${doc_DATA} ${EXTRA_DIST}
	tar cvfz ${PACKAGE}-${VERSION}.tar.gz ${PACKAGE}-${VERSION}
	rm -rf ${PACKAGE}-${VERSION}

# bikemake: serves similar purpose as automake, but is much less resource hungry
