-- functions necessary for osmosis analysers

CREATE OR REPLACE FUNCTION ends(nodes bigint[]) RETURNS SETOF bigint AS $$
DECLARE BEGIN
    RETURN NEXT nodes[1];
    RETURN NEXT nodes[array_length(nodes,1)];
    RETURN;
END
$$ LANGUAGE plpgsql;


