# kh_proj

Collaborators: Alex Ahn, Ji Park

Environment  Requirements (recommend using Homebrew for installation):
(1) Python3
(2) Mongodb
(3) VirtualEnvironment
(4) packages : please refer to requirements.txt

Virtual Environment
- make sure to activate environment ("source venv/bin/active")

Mongodb Setup
(1) Make a directory for set up ("mkdir -p /data/db")
(2) Change permission for read/write ("chmod +x /data/db")
(3) enter "mongod --dbpath ./data/db" to run

Test Run (from "kh_proj/")
(1) "source venv/bin/active"
(2) "mongod --dbpath ./data/db"
(3) python mongodb/test_db.py
