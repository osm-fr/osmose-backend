-- Allow data loss (but not corruption) in the case of a power outage. This is okay because we need to re-run the script anyways.
SET synchronous_commit TO OFF;

-- Way nodes
\copy way_nodes FROM 'way_nodes.txt'
ALTER TABLE ONLY way_nodes ADD CONSTRAINT pk_way_nodes PRIMARY KEY (way_id, sequence_id);
CREATE INDEX idx_way_nodes_node_id ON way_nodes USING btree (node_id);
ALTER TABLE ONLY way_nodes CLUSTER ON pk_way_nodes;
