DROP TABLE IF EXISTS metainfo CASCADE;
CREATE TABLE metainfo (
    tstamp timestamp without time zone NOT NULL,
    tstamp_action timestamp without time zone NOT NULL
);
INSERT INTO metainfo VALUES ('1970-01-01 00:00:00', '1970-01-01 00:00:00');
