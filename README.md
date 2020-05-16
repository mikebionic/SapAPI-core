# The E-commerce Web application [Branch of SAPHASAP System] 
## Languages:
> Python, JavaScript

Includes:
	+ Modules support
	+ Relation database management
	+ Stable REST-Api
	+ Web Service for client applications
	+ Postgresql database support
------------------------------
Install requirements from "requirements.txt" file, or simply type:
> pip3 install -r requirements.txt
------------------------------
Install Python, Python-venv and pip3:
> sudo apt install python3-dev python3-venv python3-pip
------------------------------ 
Install Postgresql on linux by typing:
> sudo apt install postgresql postgresql-contrib libpq-dev pgadmin3
------------------------------
Set the db and secrets configurations in "config.py" file
------------------------------
Initial Company and Division migrations (uncomment the lines first):
> python3 migrate.py
-----------------------------
You can also use the ready to go backup db
> commerceDBTemplate.backup
------------------------------
Rest-Api backend information:
> backend.md
------------------------------
