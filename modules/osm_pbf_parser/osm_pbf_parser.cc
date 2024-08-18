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

#include <vector>
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

  void set_since_timestamp(const uint64_t timestamp) {
      since_timestamp = timestamp;
  }

  void node_callback(uint64_t osmid, double lon, double lat, const Tags & tags, const uint64_t timestamp) {
      if (!tags.empty() && (since_timestamp == 0 || timestamp == 0 || timestamp >= since_timestamp)) {
          call_method<void>(self, "node", osmid, lon, lat, tagsToDict(tags), timestamp);
      } else {
          filtered_nodes_osmid.push_back(osmid);
      }
  }

  boost::python::list filtered_nodes() const {
      return nodeIdToList(filtered_nodes_osmid);
  }

  void way_callback(uint64_t osmid, const Tags & tags, const std::vector<uint64_t> & refs, const uint64_t timestamp) {
      if (since_timestamp == 0 || timestamp == 0 || timestamp >= since_timestamp) {
          call_method<void>(self, "way", osmid, tagsToDict(tags), nodeIdToList(refs), timestamp);
      } else {
          filtered_ways_osmid.push_back(osmid);
      }
  }

  boost::python::list filtered_ways() const {
      return nodeIdToList(filtered_ways_osmid);
  }

  void relation_callback(uint64_t osmid, const Tags & tags, const References & refs, const uint64_t timestamp) {
      if (since_timestamp == 0 || timestamp == 0 || timestamp >= since_timestamp) {
          call_method<void>(self, "relation", osmid, tagsToDict(tags), referencesToDict(refs), timestamp);
      } else {
          filtered_relations_osmid.push_back(osmid);
      }
  }

  boost::python::list filtered_relations() const {
      return nodeIdToList(filtered_relations_osmid);
  }

 private:
    PyObject* self;
    uint64_t since_timestamp = 0;
    std::vector<uint64_t> filtered_nodes_osmid;
    std::vector<uint64_t> filtered_ways_osmid;
    std::vector<uint64_t> filtered_relations_osmid;
};


BOOST_PYTHON_MODULE(osm_pbf_parser)
{
    class_<Visitor, Visitor>("Visitor")
        .def("set_since_timestamp", &Visitor::set_since_timestamp)
        .def("node", &Visitor::filtered_nodes)
        .def("filtered_nodes", &Visitor::filtered_nodes)
        .def("way", &Visitor::way_callback)
        .def("filtered_ways", &Visitor::filtered_ways)
        .def("relation", &Visitor::relation_callback)
        .def("filtered_relations", &Visitor::filtered_relations)
    ;

    def("read_osm_pbf", read_osm_pbf<Visitor>);
}
