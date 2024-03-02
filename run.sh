#!/bin/bash

run() {
    gunicorn main:app --workers 4 --threads 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7999 --timeout 600
}

run_daemon() {
    gunicorn main:app --workers 4 --threads 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7999 --timeout 600 --daemon
}

run_config() {
    gunicorn --config ./gunicorn.conf.py
}
# ps ax | grep gunicorn | awk '{print $1}' | xargs kill
case $1 in
--daemon) run_daemon ;;
--config) run_config ;;
*) run ;;
esac
