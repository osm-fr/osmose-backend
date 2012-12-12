--This function will be triggered after way update
CREATE OR REPLACE FUNCTION osmosis_ways_update_polygon() RETURNS trigger
AS $$
BEGIN
  IF NEW.linestring IS NOT NULL THEN
    NEW.is_polygon = ways_is_polygon(NEW.nodes, NEW.linestring, NEW.tags);
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

