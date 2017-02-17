------------------------------------------------------------------------------
-- Frédéric Rodrigo - 2010
-- Add key indexes on tags tables - full content index
------------------------------------------------------------------------------

CREATE INDEX idx_nodes_tags ON nodes USING gist(tags) WHERE tags != ''::hstore;
CREATE INDEX idx_nodes_addr_housenumber ON nodes USING gist(tags) WHERE tags != ''::hstore AND tags ?| ARRAY['addr:housenumber', 'addr:housename'];
CREATE INDEX idx_nodes_addr_street ON nodes USING gist(tags) WHERE tags != ''::hstore AND tags ?| ARRAY['addr:street', 'addr:district', 'addr:quarter', 'addr:suburb', 'addr:place', 'addr:hamlet'];

CREATE INDEX idx_ways_tags ON ways USING gist(tags) WHERE tags != ''::hstore;
CREATE INDEX idx_ways_highway ON ways USING gist(tags) WHERE tags != ''::hstore AND tags?'highway';
CREATE INDEX idx_ways_waterway ON ways USING gist(tags) WHERE tags != ''::hstore AND tags?'waterway';
CREATE INDEX idx_ways_natural ON ways USING gist(tags) WHERE tags != ''::hstore AND tags?'natural';
CREATE INDEX idx_ways_name ON ways USING gist(tags) WHERE tags != ''::hstore AND tags?'name';
CREATE INDEX idx_ways_building ON ways USING gist(tags) WHERE tags != ''::hstore AND tags?'building';
CREATE INDEX idx_ways_power ON ways USING gist(tags) WHERE tags != ''::hstore AND tags?'power';
CREATE INDEX idx_ways_boundary ON ways USING gist(tags) WHERE tags != ''::hstore AND tags?'boundary';
CREATE INDEX idx_ways_landuse ON ways USING gist(tags) WHERE tags != ''::hstore AND tags?'landuse';
CREATE INDEX idx_ways_addr_housenumber ON ways USING gist(tags) WHERE tags != ''::hstore AND tags ?| ARRAY['addr:housenumber', 'addr:housename'];
CREATE INDEX idx_ways_addr_street ON ways USING gist(tags) WHERE tags != ''::hstore AND tags ?| ARRAY['addr:street', 'addr:district', 'addr:quarter', 'addr:suburb', 'addr:place', 'addr:hamlet'];

CREATE INDEX idx_relations_tags ON relations USING gist(tags);
