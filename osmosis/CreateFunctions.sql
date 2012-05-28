-- functions necessary for osmosis analysers

CREATE OR REPLACE FUNCTION ends(nodes bigint[]) RETURNS SETOF bigint AS $$
DECLARE BEGIN
    RETURN NEXT nodes[1];
    RETURN NEXT nodes[array_length(nodes,1)];
    RETURN;
END
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION way_locate(linestring geometry) RETURNS geometry AS $$
DECLARE BEGIN
    IF ST_IsClosed(linestring) THEN
        RETURN ST_Centroid(linestring);
    ELSE IF ST_NPoints(linestring) > 1 THEN
        RETURN ST_PointN(linestring, (ST_NPoints(linestring)/2)::integer + 1);
    END IF;
    END IF;
END
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION relation_locate(rid bigint) RETURNS geometry AS $$
DECLARE BEGIN
    RETURN
    (SELECT
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
            relation_members.relation_id = rid
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
            relation_members.relation_id = rid
        LIMIT 1
    )) AS a
    LIMIT 1);
END
$$ LANGUAGE plpgsql;
