#!/bin/bash

echo "Descargando el modelo en_core_web_trf para spaCy..."
python3 -m spacy download en_core_web_trf

sleep 5

echo "Iniciando servidor FastAPI con Uvicorn..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-80}