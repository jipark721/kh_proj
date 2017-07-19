source ../venv/bin/activate
killall -9 mongod
mongod --dbpath mongodb/db/data & python run.py
