TRUNCATE actions;
INSERT INTO actions (SELECT 'R', 'C', id FROM relations);
INSERT INTO actions (SELECT 'W', 'C', id FROM ways);
INSERT INTO actions (SELECT 'N', 'C', id FROM nodes);
