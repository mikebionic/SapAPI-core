from utils.scraper_pack import *

from main_pack import create_app

app = create_app()
app.app_context().push()

main_parser()