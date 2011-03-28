ALTER TABLE ways ADD COLUMN is_polygon boolean;

UPDATE ways SET is_polygon = (ST_IsClosed(linestring) AND ST_NumPoints(linestring) > 3);

CREATE INDEX idx_ways_is_polygon ON ways USING btree (is_polygon);

UPDATE ways SET linestring = ST_MakePolygon(linestring) WHERE is_polygon;


-- ajout d'un index sur la table ways
create index ways_tags on ways using gist(tags);

