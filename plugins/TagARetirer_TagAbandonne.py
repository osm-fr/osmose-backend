#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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

class plugin:
    
    err_100    = 4010
    err_100_fr = u"Tag abandonné"
    err_100_en = u"Disused Tag"
    
    def node(self, data, tags):

        err = []
        
        #if u"abutters" in tags:
        #    err.append((100, 0, u"abutters=* => landuse=*"))
        
        if u"code_insee" in tags:
            err.append((100, 1000, {"en": u"code_insee => ref:INSEE"}))
        if u"code_INSEE" in tags:
            err.append((100, 1001, {"en": u"code_INSEE => ref:INSEE"}))                    
        
        if u"amenity" in tags:
            if tags[u"amenity"] == u"store":
                err.append((100, 10, {"en": u"amenity=store => shop=*"}))
            elif tags[u"amenity"] == u"supermarket":
                err.append((100, 11, {"en": u"amenity=supermarket => shop=supermarket"}))
            elif tags[u"amenity"] == u"bakers":
                err.append((100, 12, {"en": u"amenity=bakers => shop=bakery"}))
            elif tags[u"amenity"] == u"butchers":
                err.append((100, 13, {"en": u"amenity=butcher => shop=butcher"}))
                
        if u"class" in tags:
            err.append((100, 20, {"en": u"class=* => highway=*"}))
            
        if u"highway" in tags:
            if tags[u"highway"] == u"gate":
                err.append((100, 30, {"en": u"highway=gate => barrier=*"}))
            elif tags[u"highway"] == u"stile":
                err.append((100, 31, {"en": u"highway=stile => barrier=*"}))
            elif tags[u"highway"] == u"cattle_grid":
                err.append((100, 32, {"en": u"highway=cattle_grid => barrier=*"}))
            elif tags[u"highway"] == u"toll_booth":
                err.append((100, 33, {"en": u"highway=toll_booth => barrier=*"}))
            elif tags[u"highway"] == u"gate":
                err.append((100, 34, {"en": u"highway=gate => barrier=*"}))
            elif tags[u"highway"] == u"viaduct":
                err.append((100, 35, {"en": u"highway=viaduct => bridge=*"}))
            elif tags[u"highway"] == u"unsurfaced":
                err.append((100, 36, {"en": u"highway=unsurfaced => highway=* + surface=unpaved | highway=track"}))
            elif tags[u"highway"] == u"minor":
                err.append((100, 37, {"en": u"highway=minor => highway=*"}))
            elif tags[u"highway"] == u"bridge":
                err.append((100, 38, {"en": u"highway=bridge => highway=* + bridge=yes"}))
                
        if u"historic" in tags:
            if tags[u"historic"] == u"museum":
                err.append((100, 40, {"en": u"historic=museum => tourism=museum"}))
            elif tags[u"historic"] == u"icon":
                err.append((100, 41, {"en": u"historic=icon => ?"}))
                
        if u"landuse" in tags:
            if tags[u"landuse"] == u"wood":
                err.append((100, 50, {"en": u"landuse=wood => landuse=forest"}))

        if u"man_made" in tags:
            if tags[u"man_made"] == u"power_wind":
                err.append((100, 60, {"en": u"man_made=power_wind => power=generator + power_source=wind"}))
            elif tags[u"man_made"] == u"power_hydro":
                err.append((100, 61, {"en": u"man_made=power_hydro => power=generator + power_source=hydro"}))
            elif tags[u"man_made"] == u"power_fossil":
                err.append((100, 62, {"en": u"man_made=power_fossil => power=generator + power_source=*"}))
            elif tags[u"man_made"] == u"power_nuclear":
                err.append((100, 63, {"en": u"man_made=power_nuclear => power=generator + power_source=nuclear"}))
    
        if u"natural" in tags:
            if tags[u"natural"] == u"marsh":
                err.append((100, 70, {"en": u"natural=marsh => natural=wetland, wetland=*"}))

        if u"railway" in tags:
            if tags[u"railway"] == u"viaduct":
                err.append((100, 80, {"en": u"railway=viaduct => bridge=*"}))
            elif tags[u"railway"] == u"preserved_rail":
                err.append((100, 81, {"en": u"railway=preserved_rail => railway=preserved"}))
                
        if u"route" in tags:
            if tags[u"route"] == u"ncn":
                err.append((100, 90, {"en": u"route=ncn => ncn=yes"}))

        if u"waterway" in tags:
            if tags[u"waterway"] == u"waste_disposal":
                err.append((100, 100, {"en": u"waterway=waste_disposal => amenity=waste_disposal"}))
            elif tags[u"waterway"] == u"mooring":
                err.append((100, 101, {"en": u"waterway=mooring => waterway=* + mooring=yes"}))  
            elif tags[u"waterway"] == u"water_point":
                err.append((100, 102, {"en": u"waterway=water_point => amenity=drinking_water"}))  
                
        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)
    
    def relation(self, data, tags):
        return self.node(data, tags)

