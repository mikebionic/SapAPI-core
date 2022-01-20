
import requests
import json

from main_pack.config import Config

def send_data_to_sync_server(
	payload,
	host = None,
	port = None,
	url_path = None,
	token = None,
):

	host = Config.HASAP_SYNC_HOST if not host else host
	port = Config.HASAP_SYNC_PORT if not port else port
	url_path = Config.HASAP_SYNC_URL_PATH if not url_path else url_path
	token = Config.HASAP_SYNC_SHA_KEY if not token else token

	r = requests.post(
	f"http://{host}:{port}{url_path}",
	data = json.dumps(payload),
	headers = {
		'Content-Type': 'application/json',
		'x-access-token': token,
		}
	)
	# print(r.json())