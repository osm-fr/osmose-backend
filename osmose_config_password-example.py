#-*- coding: utf-8 -*-

def set_password(config):
  for country in config.keys(): 
    for k in config[country].analyser.keys():
      config[country].analyser[k] = 'foo'
