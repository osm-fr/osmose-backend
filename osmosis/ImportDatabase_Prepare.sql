-- Nodes
ALTER TABLE nodes DROP CONSTRAINT pk_nodes;
DROP INDEX idx_nodes_geom;

-- Ways
CREATE OR REPLACE FUNCTION osmosis_ways_update_polygon() RETURNS trigger
AS $$
BEGIN
  IF NEW.linestring IS NOT NULL THEN
    NEW.is_polygon =
      array_length(NEW.nodes,1) > 3 AND
      NEW.nodes[1] = NEW.nodes[array_length(NEW.nodes,1)] AND
      ST_NumPoints(NEW.linestring) > 3 AND
      ST_IsClosed(NEW.linestring) AND
      ST_IsValid(NEW.linestring) AND
      ST_IsSimple(NEW.linestring) AND
      ST_IsValid(ST_MakePolygon(NEW.linestring)) AND
      NOT (NEW.tags?'roller_coaster' AND NEW.tags->'roller_coaster' = 'track');
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS osmosis_ways_insert ON ways;
DROP TRIGGER IF EXISTS osmosis_ways_update ON ways;

CREATE TRIGGER osmosis_ways_insert BEFORE INSERT ON ways
 FOR EACH ROW EXECUTE PROCEDURE osmosis_ways_update_polygon();

CREATE TRIGGER osmosis_ways_update BEFORE UPDATE ON ways
 FOR EACH ROW EXECUTE PROCEDURE osmosis_ways_update_polygon();

ALTER TABLE ways DROP CONSTRAINT pk_ways;
DROP INDEX idx_ways_linestring;

-- Way nodes
ALTER TABLE way_nodes DROP CONSTRAINT pk_way_nodes;
DROP INDEX idx_way_nodes_node_id;

-- Relations
ALTER TABLE relations DROP CONSTRAINT pk_relations;

-- Relation members
ALTER TABLE relation_members DROP CONSTRAINT pk_relation_members;
DROP INDEX idx_relation_members_member_id_and_type;
