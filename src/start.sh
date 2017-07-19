taskkill /f /im mongod
source ../venv/Scripts/activate
mongod --dbpath mongodb/db/data & python run.py
