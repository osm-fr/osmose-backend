#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Black Myst <black.myst@free.fr> 2011                       ##
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
###########################################################################


class Plugin(object):

    def __init__(self, father):
        self.father = father

    def init(self, logger):
        """
        Called before starting analyse.
        @param logger:
        """
        self.errors = {}
        pass

    def availableMethodes(self):
        """
        Get a list of overridden methods.
        This is usefull to optimize call from analyser_sax.
        """
        capabilities = []
        currentClass = self.__class__
        if currentClass.node!=Plugin.node: capabilities.append("node")
        if currentClass.way!=Plugin.way: capabilities.append("way")
        if currentClass.relation!=Plugin.relation: capabilities.append("relation")
        return capabilities

    def node(self, node, tags):
        """
        Called each time a node is found on data source.

        @param node: dict with details.
            example: node[u"id"], node[u"lat"], node[u"lon"], node[u"version"]
        @param tags: dict with all tags and values.
        @return: error list.
        """
        pass

    def way(self, way, tags, nodes):
        """
        Called each time a way is found on data source.

        @param way: dict with details.
            example: node[u"id"], node[u"lat"], node[u"lon"], node[u"version"]
        @param tags: dict with all tags and values.
        @param nodes: list of all nodes id.
        @return: error list.
        """
        pass

    def relation(self, relation, tags, members):
        """
        Called each time a relation is found on data source.

        @param relation: dict with details.
            example: node[u"id"], node[u"lat"], node[u"lon"], node[u"version"]
        @param tags: dict with all tags and values.
        @param members:  list of all relation members.
        @return: error list.
        """
        pass

    def end(self, logger):
        """
        Called after starting analyse.
        @param logger:
        """
        pass
