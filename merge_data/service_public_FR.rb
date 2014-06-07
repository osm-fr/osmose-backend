#!/usr/bin/ruby -w
# encoding: UTF-8

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
    add = XPath.each(xmldoc, "/Organisme/Adresse/Ligne | /Organisme/Adresse/CodePostal | /Organisme/Adresse/NomCommune").collect{ |x| x.text }.join(", ")
    lat = XPath.first(xmldoc, "/Organisme/Adresse/Localisation/Latitude")
    lon = XPath.first(xmldoc, "/Organisme/Adresse/Localisation/Longitude")
    pre = XPath.first(xmldoc, "/Organisme/Adresse/Localisation/Précision")
    acc = XPath.first(xmldoc, "/Organisme/Adresse/Accessibilité")
    if acc then
        acc = acc.attribute("type")
    end
    data = [id,pivot,add,acc] + ([nom,lat,lon,pre].collect{ |x| x ? x.text : nil })
    if lat and lon then
        print data.join("\t").sub("\n", " ").sub("\r", "") + "\n"
    end
}
