TRUNCATE actions;
INSERT INTO actions (SELECT 'R', 'C', id FROM relations WHERE tstamp > ':timestamp');
INSERT INTO actions (SELECT 'W', 'C', id FROM ways WHERE tstamp > ':timestamp');
INSERT INTO actions (SELECT 'N', 'C', id FROM nodes WHERE tstamp > ':timestamp');

UPDATE metainfo SET tstamp_action = ':timestamp';
