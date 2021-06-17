
import requests

from main_pack import create_app
from main_pack.config import Config
from main_pack.models import Db_inf

app = create_app()
app.app_context().push()


database = Db_inf.query.first()
db_guid = database.DbInfGuid if database else None

r = requests.get(
	f"{Config.SAP_SERVICE_URL}{Config.SAP_SERVICE_URL_PREFIX}/devices/fetch/?uuid={db_guid}",
	headers = {
		'Content-Type': 'application/json',
		'x-access-token': Config.SAP_SERVICE_KEY,
		}
	)