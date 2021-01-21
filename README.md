# The E-commerce Web application [Branch of SAPHASAP System] 
## Languages:

> Python >= v3.6

> JavaScript | jQuery | ReactJS

## Includes:
- [x] Stable Web-Api
- [x] Web Service for client applications
- [ ] Client Admin API
- [ ] Full feature key activation
- [x] Web-Admin UI
- [x] Web-Client UI
- [x] Modules support
- [x] n18 language support
- [x] File management and compression
- [x] Security and crypting
- [x] Relation database management
- [x] Postgresql database support
- [x] Redis session support
- [x] Redis db-cache support
- [ ] Websockets support
-----------------------------

## TODO:

- [ ] Write admin client app
- [x] Prevent 500 server errors
- [x] Send Server errors by e-mail
- [x] Configure BCrypt usage toggler
- [ ] Reconfigure app and separate API with UI
	- [ ] Build separate Repo for API
	- [ ] Build separate Repo for UI
	- [ ] Rebuild a new repo for Flask-style app
	- [ ] Optimize app using NodeJs

- [ ] Database updates:
	- [x] User's last logged in, device, etc
	- [ ] App Configs migrated to db


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
**Install Redis by typing:**
```bash
sudo apt install redis
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
Sensitive informations are loaded from "[.env](/main_pack/.env.example.config)" file
Sensitive informations never shared if added to "[.gitignore](/.gitignore)" file
**Configure site settings** in main_pack/static/web_config:
	- Add robots.txt
	- Add sitemap.xml
	- Add watermark.png

Initial Company and Division migrations (uncomment the lines first):
```bash
python3 migrate.py
```
You can also use the ready to go backup db
```bash
commerceDBTemplate.backup
```

In case if flask-mail is not working well, check this configuration:
```url
https://www.google.com/settings/security/lesssecureapps
```
------------
## Info and logs
**Rest-Api backend information:**

+ [API backend](/documentation/api_backend.md)
+ [API documentation](/documentation/api_documentation.md)
+ [sap_api_server_setup](/documentation/sap_api_server_setup.md)
+ [mail_setup](/documentation/mail_setup.md)

**logs information**
+ [order invoice logs](/documentation/order_invoice_post_request_logs.md)
+ [checkout invoice logs](/documentation/checkout_order_inv_api_logs.md)

**translations and language creation**
+ [py-Babel usage](/documentation/pybabel_usage.md)
