CXX = g++

CXXFLAGS = -O3 -std=c++0x -Wall -Wextra

PYTHON_VERSION_M = $(shell python --version 2>&1 | sed -e 's/Python \([0-9]\).*/\1/')
PYTHON_VERSION_MN = $(shell python --version 2>&1 | sed -e 's/Python \([0-9]\)\.\([0-9]\+\).*/\1\2/')




all: osm_pbf_parser.so

osm_pbf_parser.so: osm_pbf_parser.cc osmpbfreader.h
	@# Detection of -lboost_python option to use is done by lanching gcc, which
	@# generates a different error message if it cannot find library.
	@BOOST_LIB1=boost_python-py$(PYTHON_VERSION_MN); \
	BOOST_LIB2=boost_python$(PYTHON_VERSION_MN); \
	if [ "`LANG=C gcc -l$$BOOST_LIB1 2>&1 | grep -c 'undefined reference to .main.'`" -eq 1 ]; then \
	  BOOST_LIB=$$BOOST_LIB1; \
	elif [ "`LANG=C gcc -l$$BOOST_LIB2 2>&1 | grep -c 'undefined reference to .main.'`" -eq 1 ]; then \
	  BOOST_LIB=$$BOOST_LIB2; \
	else \
	  echo Cannot find boost_python library from $$BOOST_LIB1 or $$BOOST_LIB2; \
	  exit 1; \
	fi; \
	LDFLAGS="-shared -l$$BOOST_LIB `pkg-config --libs --cflags protobuf-lite python$(PYTHON_VERSION_M)` -losmpbf -lz -fPIC"; \
	echo $(CXX) $(CXXFLAGS) -o $@ $< $$LDFLAGS; \
	$(CXX) $(CXXFLAGS) -o $@ $< $$LDFLAGS

clean:
	rm -f osm_pbf_parser.so
