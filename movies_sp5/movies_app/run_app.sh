#!/usr/bin/env bash

#sh init_es.sh
cd src
#gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
uvicorn main:app --host 0.0.0.0 --port 80
