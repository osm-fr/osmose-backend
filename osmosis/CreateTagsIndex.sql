------------------------------------------------------------------------------
-- Frédéric Rodrigo - 2010
-- Add key indexes on tags tables - full content index
------------------------------------------------------------------------------

CREATE INDEX idx_nodes_tags ON nodes USING gist(tags);
CREATE INDEX idx_ways_tags ON ways USING gist(tags);
CREATE INDEX idx_relations_tags ON relations USING gist(tags);
