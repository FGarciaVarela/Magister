#!/bin/bash

# Guardar el directorio actual como el directorio raíz del proyecto
PROJECT_DIR=$(pwd)

# Navegar al directorio del backend y iniciar FastAPI
echo "Iniciando backend FastAPI..."
cd "$PROJECT_DIR/src" && uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Esperar un momento para asegurar que el backend ha iniciado
sleep 5

# Navegar explícitamente de vuelta al directorio raíz del proyecto para arrancar el frontend
echo "Iniciando frontend Vite..."
cd "$PROJECT_DIR" && yarn build &

# Esperar a que cualquier proceso termine
wait $BACKEND_PID
