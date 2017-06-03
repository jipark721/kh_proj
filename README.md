# kh_proj

### Collaborators: Alex Ahn, Ji Park

## Simple Set Up:

1. "./init_proj.sh"
2. "source venv/bin/activate"
3. "mongod --dbpath ./data/db" (keep it running on a new terminal for local server hosting)
4. "cd mongodb" -> "./init_db.sh"

## Environment  Requirements (recommend using Homebrew for installation):

- Python3
- Mongodb
- VirtualEnvironment
- packages : please refer to requirements.txt

## Virtual Environment

- make sure to activate environment ("source venv/bin/activate")

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
