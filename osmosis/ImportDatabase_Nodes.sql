-- Allow data loss (but not corruption) in the case of a power outage. This is okay because we need to re-run the script anyways.
SET synchronous_commit TO OFF;

-- Nodes
\copy nodes FROM 'nodes.txt'
ALTER TABLE ONLY nodes ADD CONSTRAINT pk_nodes PRIMARY KEY (id);
CREATE INDEX idx_nodes_geom ON nodes USING gist (geom);
ALTER TABLE ONLY nodes CLUSTER ON idx_nodes_geom;
ANALYZE nodes;
