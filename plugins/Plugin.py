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
        Cette méthode est appelé avant le début de l'analyse.
        @param logger: 
        """
        pass

    def availableMethodes(self):
        """
        Get a list of overrided methodes.
        This is usefull to optimize call from analyser_sax 
        """
        capabilities = []
        currentClass = self.__class__
        if currentClass.node!=Plugin.node: capabilities.append("node")
        if currentClass.way!=Plugin.way: capabilities.append("way")
        if currentClass.relation!=Plugin.relation: capabilities.append("relation")
        return capabilities
    
    
    def node(self, node, tags):
        """
        Cette méthode est appelé à chaque fois qu'un noeud est trouvé dans
        le fichier que l'on analyse.
        
        @param node: une map contenant les informations sur le noeud.
            exemple: node[u"id"], node[u"lat"], node[u"lon"], node[u"version"]
        @param tags: une map contenant l'ensemble des clés/valeurs du noeud. 
        @return: list des erreurs lié à ce noeud
        """
        pass
    
    def way(self, way, tags, nodes):
        """
        Cette méthode est appelé à chaque fois qu'un chemin est trouvé dans
        le fichier que l'on analyse.
        
        @param way: une map contenant les informations sur le chemin.
            exemple: node[u"id"], node[u"version"]
        @param tags: une map contenant l'ensemble des clés/valeurs du chemin.
        @param nodes: une liste de tous les noeuds constituant le chemin 
        @return: list des erreurs lié à ce chemin
        """
        pass
            
    def relation(self, relation, tags, members):
        """
        Cette méthode est appelé à chaque fois qu'une relation est trouvé dans
        le fichier que l'on analyse.
        
        @param relation: une map contenant les informations sur la relation.
            exemple: node[u"id"], node[u"version"]
        @param tags: une map contenant l'ensemble des clés/valeurs de la relation.
        @param members:  liste de tous les membres de la relation
        @return: list des erreurs lié à cette relation
        """
        pass
    
    
    def end(self, logger):
        """
        Cette méthode est appelé à la fin de l'analyse.
        @param logger: 
        """
        pass
