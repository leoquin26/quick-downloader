#!/bin/bash
# start.sh

# Inicia Uvicorn directamente
echo "Starting Uvicorn..."
uvicorn app.__init__:app --host 0.0.0.0 --port 5000