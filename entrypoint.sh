#!/bin/bash
set +euo pipefail

eval "$(pdm --pep582)"

python src/manage.py migrate && \
python src/manage.py loaddata \
    area_atuacao.json \
    cargos.json \
    estados_civis.json \
    formas_contratacao.json \
    generos.json \
    turnos.json \
    ufs.json && \
python src/manage.py createsuperuser --no-input

exec python src/manage.py runserver 0.0.0.0:8000
