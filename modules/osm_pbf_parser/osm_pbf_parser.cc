/*#########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2019                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
#########################################################################*/

#include <boost/python.hpp>
using namespace boost::python;

#include "osmpbfreader.h"

using namespace CanalTP;

inline boost::python::object stringToUnicode(std::string s) {
    return boost::python::object(boost::python::handle<>(PyUnicode_FromString(s.c_str())));
}

boost::python::dict tagsToDict(const Tags & map) {
    boost::python::dict dictionary;
    for (const auto & i: map) {
        dictionary[stringToUnicode(i.first)] = stringToUnicode(i.second);
    }
    return dictionary;
}

boost::python::list nodeIdToList(const std::vector<uint64_t> & refs) {
    boost::python::list list;
    for (const auto & i: refs) {
        list.append(i);
    }
    return list;
}

boost::python::list referencesToDict(const References & refs) {
    boost::python::list list;
    for (const auto & i: refs) {
        boost::python::dict dictionary;
        dictionary["ref"] = i.member_id;
        dictionary["role"] = stringToUnicode(i.role);
        switch(i.member_type) {
            case OSMPBF::Relation::NODE : dictionary["type"] = "node";
                break;
            case OSMPBF::Relation::WAY : dictionary["type"] = "way";
                break;
            case OSMPBF::Relation::RELATION : dictionary["type"] = "relation";
                break;
        }
        list.append(dictionary);
    }
    return list;
}

struct Visitor
{
  Visitor() {}

  Visitor(PyObject *p) : self(p) {}

  Visitor(PyObject *p, const Visitor & x) : self(p) {
    (void)x;
  }

  void node_callback(uint64_t osmid, double lon, double lat, const Tags & tags) const {
      if (!tags.empty()) { // TODO Move this check earlier
          call_method<void>(self, "node", osmid, lon, lat, tagsToDict(tags));
      }
  }

  void way_callback(uint64_t osmid, const Tags & tags, const std::vector<uint64_t> & refs) const {
      call_method<void>(self, "way", osmid, tagsToDict(tags), nodeIdToList(refs));
  }

  void relation_callback(uint64_t osmid, const Tags & tags, const References & refs) const {
      call_method<void>(self, "relation", osmid, tagsToDict(tags), referencesToDict(refs));
  }

 private:
    PyObject* self;
};


BOOST_PYTHON_MODULE(osm_pbf_parser)
{
    class_<Visitor, Visitor>("Visitor")
        .def("node", &Visitor::node_callback)
        .def("way", &Visitor::way_callback)
        .def("relation", &Visitor::relation_callback)
    ;

    def("read_osm_pbf", read_osm_pbf<Visitor>);
}
