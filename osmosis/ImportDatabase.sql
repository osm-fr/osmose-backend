-- Allow data loss (but not corruption) in the case of a power outage. This is okay because we need to re-run the script anyways.
SET synchronous_commit TO OFF;

-- Users
\copy users FROM 'users.txt'

-- Nodes
ALTER TABLE nodes DROP CONSTRAINT pk_nodes;
DROP INDEX idx_nodes_geom;
\copy nodes FROM 'nodes.txt'
ALTER TABLE ONLY nodes ADD CONSTRAINT pk_nodes PRIMARY KEY (id);
CREATE INDEX idx_nodes_geom ON nodes USING gist (geom);
ALTER TABLE ONLY nodes CLUSTER ON idx_nodes_geom;
ANALYZE nodes;

-- Ways
ALTER TABLE ways DROP CONSTRAINT pk_ways;
DROP INDEX idx_ways_linestring;
\copy ways (id, version, user_id, tstamp, changeset_id, tags, nodes, linestring) FROM 'ways.txt'
ALTER TABLE ONLY ways ADD CONSTRAINT pk_ways PRIMARY KEY (id);
ALTER TABLE ONLY way_nodes CLUSTER ON pk_way_nodes;
CREATE INDEX idx_ways_linestring ON ways USING gist (linestring);
ALTER TABLE ONLY ways CLUSTER ON idx_ways_linestring;
ANALYZE ways;

-- Way nodes
ALTER TABLE way_nodes DROP CONSTRAINT pk_way_nodes;
DROP INDEX idx_way_nodes_node_id;
\copy way_nodes FROM 'way_nodes.txt'
ALTER TABLE ONLY way_nodes ADD CONSTRAINT pk_way_nodes PRIMARY KEY (way_id, sequence_id);
CREATE INDEX idx_way_nodes_node_id ON way_nodes USING btree (node_id);

-- Relations
ALTER TABLE relations DROP CONSTRAINT pk_relations;
\copy relations FROM 'relations.txt'
ALTER TABLE ONLY relations ADD CONSTRAINT pk_relations PRIMARY KEY (id);
ANALYZE relations;

-- Relation members
ALTER TABLE relation_members DROP CONSTRAINT pk_relation_members;
DROP INDEX idx_relation_members_member_id_and_type;
\copy relation_members FROM 'relation_members.txt'
ALTER TABLE ONLY relation_members ADD CONSTRAINT pk_relation_members PRIMARY KEY (relation_id, sequence_id);
CREATE INDEX idx_relation_members_member_id_and_type ON relation_members USING btree (member_id, member_type);
ALTER TABLE ONLY relation_members CLUSTER ON pk_relation_members;
