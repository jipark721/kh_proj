# kh_proj

### Collaborators: Alex Ahn, Ji Park

## Simple Set Up:

1. "./init_proj.sh"
2. "mongod --dbpath ./data/db"
3. "cd mongodb"
4. "./init_db.sh"

## Environment  Requirements (recommend using Homebrew for installation):

- Python3
- Mongodb
- VirtualEnvironment
- packages : please refer to requirements.txt

## Virtual Environment

- make sure to activate environment ("source venv/bin/active")

## Mongodb Setup

- Make a directory for set up ("mkdir -p /data/db")
- Change permission for read/write ("chmod +x /data/db")
- enter "mongod --dbpath ./data/db" to run

## Initializing DB

1. Store necessary excel files under /xls
2. run "init_db.sh"

## Test Run (from "kh_proj/")

- "source venv/bin/active"
- "mongod --dbpath ./data/db"
- "python mongodb/test_db.py"
