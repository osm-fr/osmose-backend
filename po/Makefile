PYFILES=$(shell find .. -name '*.py' -not -type l | sort)
LANG=es fr

PO=$(foreach l,$(LANG),$(l).po)

.PRECIOUS: $(PO)

all: $(PO)

osmose-backend.pot: $(PYFILES)
	LANG=C xgettext -cTRANSLATORS --language=Python --keyword=_ --keyword=N_ --keyword=T_ --force-po --output=$@.tmp $(PYFILES)
	if test -e $@; then \
	  diff -I ".*POT-Creation-Date:.*" $@ $@.tmp || cp $@.tmp $@; \
	else \
	  cp $@.tmp $@; \
	fi;

%.po: osmose-backend.pot
	if test -e $@; then \
	  msgmerge -o $@ $@ $<; \
	else \
	  msginit --locale=$(patsubst %.po,%,$@) --input=$< --output=$@; \
	fi;

statistics:
	@for i in $(PO); do \
	  (msgfmt --statistics --verbose -o - $$i > /dev/null) 2>&1; \
	done
