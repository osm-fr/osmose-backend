ALTER TABLE ways ADD COLUMN is_polygon boolean;

CREATE OR REPLACE FUNCTION ways_is_polygon(nodes bigint[], linestring geometry, tags hstore)
RETURNS BOOLEAN
AS $$
BEGIN
  RETURN (array_length(nodes,1) > 3 AND
          nodes[1] = nodes[array_length(nodes,1)] AND
          ST_NumPoints(linestring) > 3 AND ST_IsClosed(linestring) AND
          ST_IsValid(linestring) AND ST_IsSimple(linestring) AND
          ST_IsValid(ST_MakePolygon(linestring)) AND
          NOT (tags ? 'attraction' AND tags->'attraction' = 'roller_coaster'));
END
$$ LANGUAGE plpgsql;

UPDATE ways SET is_polygon = ways_is_polygon(nodes, linestring, tags);

CREATE INDEX idx_ways_is_polygon ON ways USING btree (is_polygon);

-- UPDATE ways SET linestring = ST_MakePolygon(linestring) WHERE is_polygon;
