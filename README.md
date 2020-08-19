# The E-commerce Web application [Branch of SAPHASAP System] 
## Languages:

> Python >= v3.6

> JavaScript | jQuery | ReactJS

## Includes:
+ Stable Web-Api
+ Web Service for client applications
+ Web-Admin UI
+ Web-Client UI
+ Modules support
+ n18 language support
+ File management and compression
+ Security and crypting
+ Relation database management
+ Postgresql database support
-----------------------------
## Installing
**Install Python, Python-venv and pip3:**
```bash
sudo apt install python3-dev python3-venv python3-pip
```
**Install Postgresql on linux by typing:**
```bash
sudo apt install postgresql postgresql-contrib libpq-dev
```
**Create python virtual enviroment**
```bash
python3 -m venv example_env
```
**Activate python virtual environment**
```bash
source example_env/bin/activate
```
**Install requirements from "[requirements.txt](/documentation/requirements.txt)" file, or simply type:**
```bash
pip3 install -r documentation/requirements.txt
```
or try with a [command](/documentation/pip_installation_command.md) in terminal

--------------
## Configuring

Set configurations in "[config.py](/main_pack/config.py)" file
Sensitive informations are loaded from "[.env](/.env)" file
Sensitive informations never shared if added to "[.gitignore](/.gitignore)" file

Initial Company and Division migrations (uncomment the lines first):
```bash
python3 migrate.py
```
You can also use the ready to go backup db
```bash
commerceDBTemplate.backup
```
------------
## Info and logs
**Rest-Api backend information:**

+ [backend](/documentation/backend.md)
+ [newBackend](/documentation/newBackend.md)
+ [sap_api_server_setup](/documentation/sap_api_server_setup.md)
+ [mail_setup](/documentation/mail_setup.md)

**logs information**
+ [order invoice logs](/documentation/order_invoice_post_request_logs.md)
+ [checkout invoice logs](/documentation/checkout_order_inv_api_logs.md)

**translations and language creation**
+ [py-Babel usage](/documentation/pybabel_usage.md)