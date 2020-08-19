from flask import Blueprint
from main_pack.config import Config

bp = Blueprint('commerce_auth', __name__)
url_prefix = Config.COMMERCE_URL_PREFIX

from main_pack.commerce.auth import (routes,
																		admin_auth)