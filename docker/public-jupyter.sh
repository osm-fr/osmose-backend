#!/bin/bash
set -e

docker-compose down -v
docker-compose -f docker-compose.yml -f docker-compose-dev.yml run -p 8888:8888 --rm backend ./osmose_run.py --no-clean --country=monaco --skip-analyser --skip-upload

docker-compose down
docker-compose -f docker-compose.yml -f docker-compose-dev.yml -f docker-compose-readonly.yml up -d
docker-compose -f docker-compose.yml -f docker-compose-dev.yml -f docker-compose-readonly.yml exec postgis bash /postgres-readonly.sh
docker-compose -f docker-compose.yml -f docker-compose-dev.yml -f docker-compose-readonly.yml run -p 8888:8888 --rm backend jupyter-notebook
