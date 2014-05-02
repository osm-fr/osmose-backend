PYFILES=$(shell find .. -name '*.py' -not -type l | sort)

PO:=$(wildcard *.po)

.PRECIOUS: $(PO)

all: osmose-backend.pot %.po

osmose-backend.pot: $(PYFILES)
	LANG=C xgettext -cTRANSLATORS --language=Python --keyword=_ --keyword=N_ --keyword=T_ --force-po --output=$@.tmp $(PYFILES)
	if test -e $@; then \
	  diff -I ".*POT-Creation-Date:.*" $@ $@.tmp || cp $@.tmp $@; \
	else \
	  cp $@.tmp $@; \
	fi;

%.po:
	tx pull -a --minimum-perc=75

statistics:
	@for i in $(PO); do \
	  (msgfmt --statistics --verbose -o - $$i > /dev/null) 2>&1; \
	done
