SETUP=python setup.py
all:
	$(SETUP) build

check: check-nonm
	for T in test/test02*.py; do $$T; done

check-nonm:
	for T in `find . -name \*.py | xargs grep -l '>>>'`; do python $$T; done
	for T in test/test01*.py; do $$T; done

install:
	$(SETUP) install

dist:
	$(SETUP) sdist
	cp -a cnetworkmanager.spec cnetworkmanager.changes dist

notes:
	find -name \*.py | xargs grep -nH -E 'TODO|FIXME'

doc:
	epydoc --config epydoc.cfg

.PHONY: all check check-nonm install dist notes doc
