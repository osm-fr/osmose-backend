--CREATE UNIQUE INDEX idx_actions ON actions (data_type, id);

DROP TABLE IF EXISTS transitive_touched CASCADE;
CREATE TABLE transitive_touched (
    data_type character(1),
    id bigint,
    PRIMARY KEY(data_type, id)
)
;

-- Row touched nodes, create or modify only
INSERT INTO transitive_touched
SELECT
    'N',
    id
FROM
    actions_bak
WHERE
    data_type = 'N' AND
    action IN ('C', 'M')
;


INSERT INTO transitive_touched
(
-- Row touched ways, create or modify only
SELECT
    'W',
    id
FROM
    actions_bak
WHERE
    data_type = 'W' AND
    action IN ('C', 'M')
)
UNION
(
-- touched ways from nodes
SELECT
    DISTINCT ON (id)
    'W',
    way_nodes.way_id AS id
FROM
    way_nodes
    JOIN actions_bak ON
        way_nodes.node_id = actions_bak.id AND
        data_type = 'N' AND
        action = 'M'
)
;

INSERT INTO transitive_touched
(
-- Row touched relation, create or modify only
SELECT
    'R',
    id
FROM
    actions_bak
WHERE
    data_type = 'R' AND
    action IN ('C', 'M')
)
UNION
(
-- touched relations from nodes
SELECT
    DISTINCT ON (id)
    'R',
    relation_members.relation_id AS id
FROM
    relation_members
    JOIN actions_bak ON
        relation_members.member_id = actions_bak.id AND
        data_type = 'N' AND
        action = 'M'
WHERE
    relation_members.member_type = 'N'
)
UNION
(
-- touched relations from touched ways
SELECT
    DISTINCT ON (id)
    'R',
    relation_members.relation_id AS id
FROM
    relation_members
    JOIN transitive_touched ON        
        transitive_touched.data_type = 'W' AND
        relation_members.member_id = transitive_touched.id
WHERE
    relation_members.member_type = 'W'
)
-- no touched relations from relations...
;


DROP VIEW IF EXISTS touched_nodes CASCADE;
CREATE VIEW touched_nodes AS
SELECT
    nodes.*
FROM
    nodes
    JOIN transitive_touched ON
        transitive_touched.data_type = 'N' AND
        nodes.id = transitive_touched.id
;

DROP VIEW IF EXISTS touched_ways CASCADE;
CREATE VIEW touched_ways AS
SELECT
    ways.*
FROM
    ways
    JOIN transitive_touched ON
        transitive_touched.data_type = 'W' AND
        ways.id = transitive_touched.id
;

DROP VIEW IF EXISTS touched_relations CASCADE;
CREATE VIEW touched_relations AS
SELECT
    relations.*
FROM
    relations
    JOIN transitive_touched ON
        transitive_touched.data_type = 'R' AND
        relations.id = transitive_touched.id
;
