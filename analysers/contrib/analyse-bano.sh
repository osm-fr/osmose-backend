. $(dirname $0)/config.sh
OUT=/home/fred/osmose/insee_bano-france.xml

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<analysers timestamp=\"`date -u +%Y-%m-%dT%H:%M:%SZ`\">
  <analyser timestamp=\"`date -u +%Y-%m-%dT%H:%M:%SZ`\">
    <class item=\"7170\" tag=\"highway\" id=\"30\" level=\"3\">
      <classtext lang=\"fr\" title=\"name=* ou route potentiellement manquante à proximité\" />
      <classtext lang=\"en\" title=\"name=* or possibly missing highway in the area\" />
    </class>
    <class item=\"7170\" tag=\"highway\" id=\"32\" level=\"3\">
      <classtext lang=\"fr\" title=\"name=* à ajouter sur highway ?\" />
      <classtext lang=\"en\" title=\"name=* to add on highway ?\" />
    </class>
    <class item=\"7170\" tag=\"highway\" id=\"31\" level=\"3\">
      <classtext lang=\"fr\" title=\"name=* à modifier sur highway ?\" />
      <classtext lang=\"en\" title=\"name=* to change on highway ?\" />
    </class>
    <class item=\"7170\" tag=\"highway\" id=\"33\" level=\"3\">
      <classtext lang=\"fr\" title=\"route manquante à proximité ?\" />
      <classtext lang=\"en\" title=\"missing highway in the area ?\" />
    </class>
" > $OUT

for d in `seq -w 1 19` 2A 2B `seq 21 95` `seq 971 976` ; do
PGOPTIONS='--client-min-messages=warning' psql osm -qc "
select * from (
select case
  when id is null
  then format('<error class=\"33\" subclass=\"%s\"><location lat=\"%s\" lon=\"%s\" /><text lang=\"fr\" value=\"%s (%s)\" /></error>',
    subclass,lat,lon,voie_cadastre,fantoir)
  when id_noname is not null and id_noname not like '%,%' and (l_geom-l_ways_noname<100) and ((l_noname > 0.5 and l2_noname<100) or (l_noname > 0.75)) and upper(voie_cadastre)!=voie_cadastre
  then format('<error class=\"32\" subclass=\"%s\"><location lat=\"%s\" lon=\"%s\" /><text lang=\"fr\" value=\"%s (%s)\" /><way id=\"%s\"></way><fixes><fix><way id=\"%s\"><tag action=\"create\" k=\"name\" v=\"%s\" /></way></fix></fixes></error>',
    subclass,lat,lon,voie_cadastre,fantoir,id_noname,id_noname,voie_cadastre)
  when id is not null and id not like '%,%' and (l_geom-l_ways<100) and ((l > 0.5 and l2 < 100) or (l>0.75)) and names is null and upper(voie_cadastre)!=voie_cadastre
    then format('<error class=\"32\" subclass=\"%s\"><location lat=\"%s\" lon=\"%s\" /><text lang=\"fr\" value=\"%s (%s)\" /><way id=\"%s\"></way><fixes><fix><way id=\"%s\"><tag action=\"create\" k=\"name\" v=\"%s\" /></way></fix></fixes></error>',
                subclass,lat,lon,voie_cadastre,fantoir,id,id,voie_cadastre)
  when id is not null and id not like '%,%' and (l_geom-l_ways<100) and ((l > 0.5 and l2 < 100) or (l>0.75)) and names is not null and upper(voie_cadastre)!=voie_cadastre
    then format('<error class=\"31\" subclass=\"%s\"><location lat=\"%s\" lon=\"%s\" /><text lang=\"fr\" value=\"%s (%s)\" /><way id=\"%s\"><tag k=\"name\" v=\"%s\" /></way><fixes><fix><way id=\"%s\"><tag action=\"modify\" k=\"name\" v=\"%s\" /></way></fix><fix><way id=\"%s\"><tag action=\"create\" k=\"ref:FR:FANTOIR\" v=\"%s\" /></way></fix></fixes></error>',
      subclass,lat,lon,voie_cadastre,fantoir,id,names,id,voie_cadastre,id,fantoir)
  when names ~* voie_cadastre then ''
  else format('<error class=\"30\" subclass=\"%s\"><location lat=\"%s\" lon=\"%s\" /><text lang=\"fr\" value=\"%s (%s)\" /></error>',
    subclass,lat,lon,voie_cadastre,fantoir)
  end as er
  from (select
      abs(('x'||md5(coalesce(nom_voie, replace(voie_cadastre,E'\x22','')) || f.fantoir || ST_AsText(geom)))::bit(64)::bigint) AS subclass,
      round(st_x(st_transform(st_centroid(geom),4326))::numeric,6) as lon, round(st_y(st_transform(st_centroid(geom),4326))::numeric,6) as lat,
      coalesce(nom_voie, replace(voie_cadastre,E'\x22','')) as voie_cadastre, f.fantoir, replace(names,E'\x22','') as names, id, id_noname,
      st_length(st_intersection(ways,st_buffer(geom,20)))/st_length(ways) as l,
      st_length(st_transform(ways,4326)::geography)-st_length(st_transform(st_intersection(ways,geom),4326)::geography) as l2,
      st_length(st_intersection(ways_noname,st_buffer(geom,20)))/st_length(ways_noname) as l_noname,
      st_length(st_transform(ways_noname,4326)::geography)-st_length(st_transform(st_intersection(ways_noname,geom),4326)::geography) as l2_noname,
      st_length(st_transform(st_longestline(geom,geom),4326)::geography) as l_geom,
      st_length(st_transform(st_longestline(ways,ways),4326)::geography) as l_ways,
      st_length(st_transform(st_longestline(ways_noname,ways_noname),4326)::geography) as l_ways_noname
    from (select m.fantoir, m.voie_cadastre, m.nb as nb_adresses, m.geom, string_agg(w.osm_id::text,',') as id, st_collect(w.way) as ways,
        st_collect(n.way) as ways_noname, string_agg(n.osm_id::text,',') as id_noname,
        max(w.name) as name, string_agg(w.name,';') as names
      from (select fantoir, voie_cadastre, count(*) as nb, st_transform(st_convexhull(st_collect(geometrie)),900913) as geom from cumul_adresses where coalesce(voie_osm,'') ='' group by 1,2) as m
      left join planet_osm_line w on ((st_intersects(w.way, geom) or st_dwithin(w.way,geom,20)) and w.highway is not null)
      left join planet_osm_line n on (n.osm_id=w.osm_id and n.name is null)
      where nb>=2 and m.fantoir ~ '^$d.*[0-9]....$'
      group by 1,2,3,4) as f
    left join statut_fantoir s on (s.fantoir=f.fantoir)
    left join (select nom_voie, code_insee||fant_voie||'%' as fantoir from ban where code_insee ~ '^$d' group by 1,2) as b on (f.fantoir like b.fantoir)
    where s.fantoir is null and coalesce(name,'') != coalesce(nom_voie, replace(voie_cadastre,E'\x22',''))
    group by geom, id, id_noname, f.fantoir, voie_cadastre, ways, ways_noname, name, names, b.nom_voie) as m order by l_noname desc, l desc) as e where er != '';
" -t >> $OUT
done

echo "  </analyser>
</analysers>" >> $OUT

curl -s --request POST --form source='opendata_xref-france' --form code="$OSMOSEPASS" --form content=@$OUT http://osmose.openstreetmap.fr/control/send-update

