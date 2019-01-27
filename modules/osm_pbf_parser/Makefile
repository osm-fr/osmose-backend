CXX = g++

CXXFLAGS = -O3 -std=c++0x -Wall -Wextra

PYTHON_VERSION_M = $(shell python --version 2>&1 | sed -e 's/Python \([0-9]\).*/\1/')
PYTHON_VERSION_MN = $(shell python --version 2>&1 | sed -e 's/Python \([0-9]\)\.\([0-9]\+\).*/\1\2/')
LDFLAGS = -shared -lboost_python-py$(PYTHON_VERSION_MN) `pkg-config --libs --cflags protobuf-lite python$(PYTHON_VERSION_M)` -losmpbf -lz -fPIC

all: osm_pbf_parser.so

osm_pbf_parser.so: osm_pbf_parser.cc osmpbfreader.h
	$(CXX) $(CXXFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f osm_pbf_parser.so
