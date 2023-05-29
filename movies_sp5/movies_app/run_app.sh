#!/usr/bin/env bash

sh init_es.sh
cd src
uvicorn main:app --host 0.0.0.0 --port 80 --workers 4
