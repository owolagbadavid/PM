#/usr/bin/env bash
#setup flask app

#Setup and activate virtual env
python -m venv pm

source pm/bin/activate

#install required packages
pip install -r requirements.txt

# Run your Flask app
python run.py