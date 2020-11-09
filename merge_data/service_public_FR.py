#!/usr/bin/env python
# coding: utf-8

import csv
import os
import xml.etree.ElementTree as ET

path = 'organismes/'

def get_poi_info(file_name):    
    print(file_name)
    root = ET.parse(file_name).getroot()

    organisme = {}
    organisme['id'] = root.get('id')
    organisme['category'] = root.get('pivotLocal')
    organisme['name'] = None
    if root.find('Nom') is not None :
        organisme['name'] = root.find('Nom').text

    organisme['email'] = None
    organisme['phone'] = None
    contact_info = root.find('CoordonnéesNum')
    if contact_info is not None:
        if contact_info.find('Email') is not None :
            organisme['email'] = contact_info.find('Email').text        
        if contact_info.find('Téléphone') is not None :
            organisme['phone'] = contact_info.find('Téléphone').text

    organisme['wheelchair_access'] = None

    for address in root.findall('Adresse'):
        address_elems = []
        name = address.findall('Ligne')
        for address_part in address.findall('Ligne'):
            address_elems.append(address_part.text)
        if address.find('CodePostal') is not None:
            address_elems.append(address.find('CodePostal').text)
        if address.find('NomCommune') is not None:
            address_elems.append(address.find('NomCommune').text)
        if address.find('Accessibilité') is not None:
            organisme['wheelchair_access'] = address.find('Accessibilité').get('type')
        geoloc = address.find('Localisation')
        if geoloc:
            organisme['latitude'] = geoloc.find('Latitude').text
            organisme['longitude'] = geoloc.find('Longitude').text
            organisme['geoloc_precision'] = int(float(geoloc.find('Précision').text))
            organisme['address'] = ', '.join(address_elems)

    return organisme


organismes = []

for r, d, f in os.walk(path):
    for file_ in f:
        if '.xml' in file_:
            file_name = os.path.join(r, file_)
            organismes.append(get_poi_info(file_name))

with open("service_public_FR.csv", 'w') as out_file:
        wr = csv.DictWriter(out_file, quoting=csv.QUOTE_ALL, fieldnames = organismes[0].keys())
        wr.writeheader()
        for a_row in organismes :
            wr.writerow(a_row)

