-- Allow data loss (but not corruption) in the case of a power outage. This is okay because we need to re-run the script anyways.
SET synchronous_commit TO OFF;

-- Ways
\copy ways (id, version, user_id, tstamp, changeset_id, tags, nodes, linestring) FROM 'ways.txt'
ALTER TABLE ONLY ways ADD CONSTRAINT pk_ways PRIMARY KEY (id);
CREATE INDEX idx_ways_linestring ON ways USING gist (linestring);
ALTER TABLE ONLY ways CLUSTER ON idx_ways_linestring;
ANALYZE ways;
