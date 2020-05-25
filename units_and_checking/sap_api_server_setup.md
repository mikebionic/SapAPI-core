
adduser iot

adduser iot sudo

apt update && apt upgrade -y && apt install python3-pip python3-venv postgresql postgresql-contrib libpq-dev -y

python3 -m venv sap_api_env
source sap_api_env/bin/activate
pip install --update pip
pip install -r requirements.txt


sudo apt install nginx python3-venv python3-dev python3-pip supervisor -y && pip3 install gunicorn
# or
apt install nginx -y && pip3 install gunicorn
# ################# update configs of nginx and gunicorn

sudo rm /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-enabled/sap_api

server {
        listen 80;
        server_name 91.201.40.64;
        location /static {
                alias /home/api/sap_api/main_pack/static;
        }
        location / {
                proxy_pass http://localhost:8000;
                include /etc/nginx/proxy_params;
                proxy_redirect off;
        }
}

sudo systemctl restart nginx

sudo nano /etc/supervisor/conf.d/sap_api.conf
# ##
[program:sap_api]
directory=/home/api/sap_api
command=/home/api/sap_api_env/bin/gunicorn -w 3 run:app
user=api
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/sap_api/sap_api.err.log
stdout_logfile=/var/log/sap_api/sap_api.out.log
# ##
sudo mkdir -p /var/log/sap_api
sudo touch /var/log/sap_api/sap_api.err.log
sudo touch /var/log/sap_api/sap_api.out.log
sudo supervisorctl reload


