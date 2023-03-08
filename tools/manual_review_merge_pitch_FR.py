"""
 This file helps to review the data used to merge information
 1. download file from https://equipements-sgsocialgouv.opendatasoft.com/explore/dataset/data-es/information/
 2. store it ad data-es.csv in the current folder
 3. run the file

other helping file:
  https://equipements-sgsocialgouv.opendatasoft.com/explore/dataset/ref-atlas/information/
    => "Permet de définir le code atlas d'un équipement à partir de son type (utilisé par le jeu de données Data ES)"
  https://equipements-sgsocialgouv.opendatasoft.com/explore/dataset/ref-caracteristiques-es/information/
    => "Décrit les caractéristiques utilisées sur les équipements sportifs (jeu de données Data ES)"
"""
import logging
import os.path

import pandas as pd

import dictionaries.fr.surface

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
log = logging.getLogger()

ES_SOURCE = "data-es.csv"
EQUIPMENT_COL = "Type d'équipement sportif"
SURFACE_COL = "Nature du sol"
MERGE_MATRIX = os.path.join("..", "merge_data", "pitch_FR.mapping.csv")
SURFACE_MAP = dictionaries.fr.surface.SURFACE

log.info("Jetzt geht's los")
log.info("Loading source files")

if os.path.exists(ES_SOURCE) is False:
    log.error(f"You must download the datasource first and store it as '{ES_SOURCE}'")
    exit()

# read specific columns of csv file using Pandas
df_es = pd.read_csv(ES_SOURCE, sep=";", usecols=[EQUIPMENT_COL, SURFACE_COL])
df_es.fillna("", inplace=True)
df_matrix = pd.read_csv(MERGE_MATRIX, sep=",", header=None, skip_blank_lines=True)
df_matrix.fillna("", inplace=True)

logging.info("Step 1: searching for missing merge values")
equipments_es = df_es[EQUIPMENT_COL].unique()
equipments_matrix = df_matrix[1].unique()

es_equipments_count = df_es[EQUIPMENT_COL].value_counts()

log.info(f"  Step 1.1: do we have all '{EQUIPMENT_COL}' in '{MERGE_MATRIX}'?")
coverage = 0
for equipment in equipments_es:
    if equipments_matrix.__contains__(equipment) is False:
        log.info(
            f"    '{equipment}' does not exist in '{MERGE_MATRIX}', it is {es_equipments_count.loc[equipment]} equipments")
    else:
        coverage += es_equipments_count.loc[equipment]
log.info(f"  -> current coverage is {coverage / df_es[EQUIPMENT_COL].count():.2%}, (missing: {df_es[EQUIPMENT_COL].count() - coverage})")

log.info(f"  Step 1.2: do we have all values from '{MERGE_MATRIX}' in '{EQUIPMENT_COL}' column?")
for equipment in equipments_matrix:
    if equipments_es.__contains__(equipment) is False:
        log.info(f"    '{equipment}' does not exist in '{ES_SOURCE}'")

del equipments_es, equipments_matrix, es_equipments_count

logging.info("Step 2: is our surface coverage exhaustive?")
surface_es = df_es[SURFACE_COL].unique()
surface_matrix = SURFACE_MAP
es_surface_count = df_es[SURFACE_COL].value_counts()

log.info(f"  Step 2.1: do we have all '{SURFACE_COL}' in '{MERGE_MATRIX}'?")
coverage = 0
for surface in surface_es:
    if surface_matrix.__contains__(surface) is False:
        log.info(f"    '{surface}' does not exist in '{MERGE_MATRIX}', it is {es_surface_count.loc[surface]} equipments")
    else:
        coverage += es_surface_count.loc[surface]
log.info(f"  -> current coverage is {coverage / df_es[SURFACE_COL].count():.2%}, (missing: {df_es[SURFACE_COL].count() - coverage})")


log.info(f"  Step 2.2: do we have all values from '{MERGE_MATRIX}' in '{SURFACE_COL}' column?")
for surface in surface_matrix:
    if surface_es.__contains__(surface) is False:
        log.info(f"    '{surface}' does not exist in {ES_SOURCE}")

del surface_es, surface_matrix, es_surface_count

log.info("Färtig !")