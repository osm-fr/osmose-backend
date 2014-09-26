#!/usr/bin/ruby -w
# encoding: UTF-8

require 'rexml/document'
include REXML
require 'csv'

xmlfile = File.new(ARGV[0])
xmldoc = Document.new(xmlfile)

  services_ = {
    'Laverie' => nil,
    'Aire de camping-cars' => nil,
    'Relais colis' => nil,
    'Douches' => nil,
    'Bar' => nil,
    'Espace bébé / change' => nil,
    'Restauration sur place' => nil,
    'Vente de pétrole lampant' => nil,
    'Location de véhicule' => nil,
    'Vente de fioul domestique' => nil,
    'Restauration à emporter' => nil,
    'Baie de service auto' => nil,
    'GPL' => nil,
    'Lavage haute-pression' => nil,
    'Lavage multi-programmes' => nil,
    'Toilettes publiques' => nil,
    'Station de lavage' => nil,
    'Piste poids lourds' => nil,
    'Carburant qualité supérieure' => nil,
    'Boutique non alimentaire' => nil,
    'Boutique alimentaire' => nil,
    'Station de gonflage' => nil,
    'Automate CB' => nil,
    'Vente de gaz domestique' => nil,
  }
  fuels_ = {
    'E85' => nil,
    'GPLc' => nil,
    'E10' => nil,
    'SP95' => nil,
    'SP98' => nil,
    'Gazole' => nil,
  }

print CSV.generate{ |csv|
  csv << [:id, :lat, :lon, :adresse, :ville, :debut, :fin, :saufjour] + services_.keys + fuels_.keys

  root = xmldoc.root
  XPath.each(root, '/pdv_liste/pdv') { |pdv|
    services = services_.dup
    fuels = fuels_.dup

    id = pdv.attribute('id').value
    lat = pdv.attribute('latitude').value
    lon = pdv.attribute('longitude').value
    adresse = XPath.first(pdv, 'adresse').text
    ville = XPath.first(pdv, 'ville').text
    debut = XPath.first(pdv, 'ouverture/@debut').value
    fin = XPath.first(pdv, 'ouverture/@debut').value
    saufjour = XPath.first(pdv, 'ouverture/@saufjour').value
    XPath.each(pdv, 'services/service').collect { |service|
      service.text
    }.each{ |service|
      services[service] = :x
    }
    XPath.each(pdv, 'prix/@nom').collect { |prix|
      prix.value
    }.each{ |prix|
      fuels[prix] = :x
    }

    csv << [id, lat.to_f/100000, lon.to_f/100000, adresse, ville, debut, fin, saufjour] + services.values + fuels.values
  }
}
