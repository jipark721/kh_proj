# kh_proj

### Collaborators: Alex Ahn, Ji Park

## Prerequisites

- Brew
- Python3

## Set up

virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements

## Run 

DB: mongod --dbpath mongodb/db/data
RUN: python run.py

## Initializing DB

1. Place all .xlsx files under ~/Downloads
2. run "init_db.sh" in at mongodb dir.

## Testing

1. run "python test_db.py" at mongodb dir.
