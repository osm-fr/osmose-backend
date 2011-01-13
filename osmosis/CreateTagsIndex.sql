------------------------------------------------------------------------------
-- Frédéric Rodrigo - 2010
-- Add key indexes on tags tables - full content index
------------------------------------------------------------------------------

CREATE INDEX idx_node_tags_k ON node_tags (k);
CREATE INDEX idx_way_tags_k ON way_tags (k);
CREATE INDEX idx_relation_tags_k ON relation_tags (k);
