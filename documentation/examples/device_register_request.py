import requests
import json

data = {'DevUniqueId': '7eacd10ba4b915a7', 'DevDesc': '', 'AddInf1': '', 'AddInf2': '', 'AddInf3': '', 'AddInf4': '', 'AddInf5': '', 'AddInf6': 'id=QP1A.190711.020,androidId=7eacd10ba4b915a7,baseOS=,release=10,brand=samsung,device=a10s,display=QP1A.190711.020.A107FXXU8BUC2,manufacturer=samsung,model=SM-A107F,isPhysicalDevice=true'}

r = requests.post(
	"http://<host>/<prefix>/api/devices/register/",
	data = json.dumps(data),
	headers = {'Content-Type': 'application/json'})