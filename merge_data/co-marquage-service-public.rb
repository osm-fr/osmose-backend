#!/usr/bin/ruby -w

# find all_20130522/organismes/ -type f | xargs ruby co-marquage-service-public.rb > co-marquage-service-public.csv

require 'rexml/document'
include REXML

ARGV.each{ |xml|
    xmlfile = File.new(xml)
    xmldoc = Document.new(xmlfile)

    root = xmldoc.root
    id = XPath.first(xmldoc, "/Organisme/@id").value
    pivot = XPath.first(xmldoc, "/Organisme/@pivotLocal").value
    nom = XPath.first(xmldoc, "/Organisme/Nom")
    lat = XPath.first(xmldoc, "/Organisme/Adresse/Localisation/Latitude")
    lon = XPath.first(xmldoc, "/Organisme/Adresse/Localisation/Longitude")
    acc = XPath.first(xmldoc, "/Organisme/Adresse/Accessibilité")
    data = [id,pivot] + ([nom,lat,lon,acc].collect{ |x| x ? x.text : nil })
    print data.join("\t") + "\n"
}
