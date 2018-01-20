PYFILES=$(shell find .. -name '*.py' -not -type l | grep -v 'MapCSS_josm_' | sort)

PO:=$(wildcard *.po)

.PRECIOUS: $(PO)

all: osmose-backend.pot %.po

osmose-backend.pot: $(PYFILES)
	sed -i "s/^#: .*//" osmose-backend.pot
	LANG=C xgettext --join-existing -cTRANSLATORS --language=Python \
          --keyword=_ --keyword=N_ --keyword=T_ --keyword=T_f --keyword=tr \
          --force-po --omit-header \
          --output=$@ $(PYFILES)

%.po:
	tx pull -a --minimum-perc=5

statistics:
	@for i in $(PO); do \
	  (msgfmt --statistics --verbose -o - $$i > /dev/null) 2>&1; \
	done
