cat etalab_cs1100507_stock_20180608-0437.csv | grep 'structureet;' | iconv -f ISO-8859-15 -t utf-8 | csvcut -d ';' -C 1 > finess-structureet.csv
cat etalab_cs1100507_stock_20180608-0437.csv | grep 'geolocalisation;' | iconv -f ISO-8859-15 -t utf-8  | csvcut -d ';' -C 1 > finess-geolocalisation.csv
echo "nofinesset,nofinessej,rs,rslongue,complrs,compldistrib,numvoie,typvoie,voie,compvoie,lieuditbp,commune,departement,libdepartement,ligneacheminement,telephone,telecopie,categetab,libcategetab,categagretab,libcategagretab,siret,codeape,codemft,libmft,codesph,libsph,dateouv,dateautor,datemaj,numuai,coordxet,coordyet,sourcecoordet,datemajcoord" > finess.csv
csvjoin --no-header-row --columns 1,1 --left finess-structureet.csv finess-geolocalisation.csv | tail -n +2 >> finess.csv
