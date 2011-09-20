-- ajout d'un index sur la table ways
CREATE INDEX ways_tags ON ways USING gist(tags);

-- crée des polygones là où il faut
ALTER TABLE ways ADD COLUMN is_polygon boolean;

UPDATE ways SET is_polygon = (ST_IsClosed(linestring) AND ST_NumPoints(linestring) > 3 AND
                              NOT (tags ? 'attraction' AND tags->'attraction' = 'roller_coaster'));

CREATE INDEX idx_ways_is_polygon ON ways USING btree (is_polygon);

UPDATE ways SET linestring = ST_MakePolygon(linestring) WHERE is_polygon;
