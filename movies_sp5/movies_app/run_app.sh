#!/usr/bin/env bash

#sh init_es.sh
until curl -sS "http://$ELASTIC_HOST:$ELASTIC_PORT/_cat/health?h=status" | grep -q "green\|yellow"; do
    sleep 5
done

cd src
uvicorn main:app --host 0.0.0.0 --port 80 --workers 4
