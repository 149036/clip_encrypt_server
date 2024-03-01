#!/bin/bash

run() {
    gunicorn main:app --workers 4 --threads 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7999 --timeout 600 --daemon
}

run
