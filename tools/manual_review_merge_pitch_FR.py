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

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
log = logging.getLogger()
ES_SOURCE = "data-es.csv"
ES_EQUIPMENT_COL_NAME = "Type d'équipement sportif"
MERGE_MATRIX = os.path.join("..", "merge_data", "pitch_FR.mapping.csv")

log.info("Loading source files")

if os.path.exists(ES_SOURCE) is False:
    log.error(f"You must download the datasource first and store it as '{ES_SOURCE}'")
    exit()

# read specific columns of csv file using Pandas
df_es = pd.read_csv(ES_SOURCE, sep=";", usecols=[ES_EQUIPMENT_COL_NAME])
df_matrix = pd.read_csv(MERGE_MATRIX, sep=",", header=None, skip_blank_lines=True)

logging.info("Step 1: searching for missing merge values")
equipments_es = df_es[ES_EQUIPMENT_COL_NAME].unique()
equipments_matrix = df_matrix[1].unique()

es_equipments_count = df_es[ES_EQUIPMENT_COL_NAME].value_counts()

log.info(f"  Step 1.1: do we have all {ES_EQUIPMENT_COL_NAME} in {MERGE_MATRIX}?")
for equipment in equipments_es:
    if equipments_matrix.__contains__(equipment) is False:
        log.info(f"    '{equipment}' does not exist in {MERGE_MATRIX}, it is {es_equipments_count.loc[equipment]} equipments")

log.info(f"  Step 1.2: do we have all values from {MERGE_MATRIX} in '{ES_EQUIPMENT_COL_NAME}' column?")
for equipment in equipments_matrix:
    if equipments_es.__contains__(equipment) is False:
        log.info(f"    '{equipment}' does not exist in {ES_SOURCE}")