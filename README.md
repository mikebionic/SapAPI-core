# The E-commerce Web application [Branch of SAPHASAP System] 
## Languages:
> Python, JavaScript

Includes:
	+ Modules support
	+ Relation database management
	+ Stable REST-Api
	+ Web Service for client applications
	+ Postgresql database support
-----------------------------
## Installing
Install requirements from "requirements.txt" file, or simply type:
```bash
pip3 install -r requirements.txt
```
Install Python, Python-venv and pip3:
```bash
sudo apt install python3-dev python3-venv python3-pip
```
Install Postgresql on linux by typing:
```bash
sudo apt install postgresql postgresql-contrib libpq-dev pgadmin3
```
-----------------------------
## Configuring
Set the db and secrets configurations in "config.py" file
Initial Company and Division migrations (uncomment the lines first):
```bash
python3 migrate.py
```
You can also use the ready to go backup db
```bash
commerceDBTemplate.backup
```
Rest-Api backend information:
```dir
backend.md
documentation/
documentation/newBackend.md
```