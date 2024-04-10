#!/bin/bash

echo "Iniciando servidor FastAPI con Uvicorn..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-80}