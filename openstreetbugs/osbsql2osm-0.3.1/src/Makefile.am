CLEANFILES = parser.h parser.c flexer.c
AM_YFLAGS = -d


flexer.c: flexer.l
	$(LEX) -o $@ flexer.l

BUILT_SOURCES = flexer.c parser.h
bin_PROGRAMS = osbsql2osm
osbsql2osm_SOURCES = parser.y 

dist_EXTRA_osbsql2osm_SOURCES = flexer.l 


