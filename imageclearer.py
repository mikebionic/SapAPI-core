import os
from main_pack import create_app

app = create_app()
app.app_context().push()

from main_pack.config import Config
from utils.imageclearer_pack import run_clearer

run_clearer(
	os.path.join(Config.STATIC_FOLDER_LOCATION, "uploads", "commerce", "Resource"),
	model_type = "image"
)

run_clearer(
	os.path.join(Config.STATIC_FOLDER_LOCATION, "uploads", "commerce", "Slider"),
	model_type = "slider"
)