-- functions necessary for osmosis analysers

CREATE OR REPLACE FUNCTION ends(nodes bigint[]) RETURNS SETOF bigint AS $$
DECLARE BEGIN
    RETURN NEXT nodes[1];
    RETURN NEXT nodes[array_length(nodes,1)];
    RETURN;
END
$$ LANGUAGE plpgsql
   IMMUTABLE
   RETURNS NULL ON NULL INPUT;


CREATE OR REPLACE FUNCTION way_locate(linestring geometry) RETURNS geometry AS $$
DECLARE BEGIN
    IF ST_NPoints(linestring) > 1 THEN
        IF ST_Length(linestring) = 0 THEN
            RETURN ST_PointN(linestring, 1);
        ELSE IF ST_IsClosed(linestring) THEN
            RETURN ST_Centroid(linestring);
        ELSE
            RETURN ST_PointN(linestring, (ST_NPoints(linestring)/2)::integer + 1);
        END IF;
        END IF;
    ELSE IF ST_NPoints(linestring) = 1 THEN
        RETURN ST_PointN(linestring, 1);
    END IF;
    END IF;
    RETURN NULL;
END
$$ LANGUAGE plpgsql
   IMMUTABLE
   RETURNS NULL ON NULL INPUT;


CREATE OR REPLACE FUNCTION relation_locate(rid bigint) RETURNS geometry AS $$
    SELECT
        geom
    FROM
    ((
        SELECT
            ST_PointN(linestring, 1) AS geom
        FROM
            relation_members
            JOIN ways ON
                relation_members.member_id = ways.id AND
                relation_members.member_type = 'W'
        WHERE
            relation_members.relation_id = $1
        LIMIT 1
    ) UNION (
        SELECT
            geom
        FROM
            relation_members
            JOIN nodes ON
                relation_members.member_id = nodes.id AND
                relation_members.member_type = 'N'
        WHERE
            relation_members.relation_id = $1
        LIMIT 1
    )) AS a
    LIMIT 1;
$$ LANGUAGE sql
   STABLE
   RETURNS NULL ON NULL INPUT;


CREATE OR REPLACE FUNCTION relation_bbox(rid bigint) RETURNS geometry AS $$
DECLARE BEGIN
    RETURN (SELECT
        ST_Envelope(ST_Collect(geom))
    FROM
    ((
        SELECT
            ST_Envelope(ST_Collect(geom)) AS geom
        FROM
            relation_members
            JOIN nodes ON
                relation_members.member_type = 'N' AND
                relation_members.member_id = nodes.id
        WHERE
            relation_members.relation_id = rid
    ) UNION (
        SELECT
            ST_Envelope(ST_Collect(linestring)) AS geom
        FROM
            relation_members
            JOIN ways ON
                relation_members.member_type = 'W' AND
                relation_members.member_id = ways.id
        WHERE
            relation_members.relation_id = rid
    )) AS t);
END
$$ LANGUAGE plpgsql
   STABLE
   RETURNS NULL ON NULL INPUT;

CREATE OR REPLACE FUNCTION relation_shape(rid bigint) RETURNS geometry AS $$
DECLARE BEGIN
    RETURN (SELECT
        ST_Collect(geom)
    FROM
    ((
        SELECT
            geom AS geom
        FROM
            relation_members
            JOIN nodes ON
                relation_members.member_type = 'N' AND
                relation_members.member_id = nodes.id
        WHERE
            relation_members.relation_id = rid
    ) UNION (
        SELECT
            linestring AS geom
        FROM
            relation_members
            JOIN ways ON
                relation_members.member_type = 'W' AND
                relation_members.member_id = ways.id
        WHERE
            relation_members.relation_id = rid
    ) UNION (
        SELECT
            (ST_Dump(poly)).geom AS geom
        FROM
        (
            SELECT
                ST_Polygonize(linestring) AS poly
            FROM
                relation_members
                JOIN ways ON
                    relation_members.member_type = 'W' AND
                    relation_members.member_id = ways.id AND
                    ST_NPoints(linestring) > 2
            WHERE
                relation_members.relation_id = rid
        ) AS g
    )) AS t);
END
$$ LANGUAGE plpgsql
   STABLE
   RETURNS NULL ON NULL INPUT;


CREATE OR REPLACE FUNCTION any_locate(type char(1), aid bigint) RETURNS geometry AS $$
    SELECT CASE $1
        WHEN 'N' THEN (SELECT geom FROM nodes WHERE nodes.id = $2)
        WHEN 'W' THEN (SELECT way_locate(linestring) FROM ways WHERE ways.id = $2)
        WHEN 'R' THEN relation_locate($2)
    END;
$$ LANGUAGE sql
   STABLE
   RETURNS NULL ON NULL INPUT;


CREATE OR REPLACE FUNCTION array_locate(many text[]) RETURNS geometry AS $$
    SELECT CASE
        WHEN $1 IS NULL THEN NULL
        ELSE any_locate(substr($1[1], 1, 1), CAST(substr($1[1], 2) AS bigint))
    END;
$$ LANGUAGE sql
   STABLE
   RETURNS NULL ON NULL INPUT;
