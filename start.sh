#/usr/bin/env bash

export FLASK_APP=run.py

flask db migrate -m "migration"

flask db upgrade

python run.py
