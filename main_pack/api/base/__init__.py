from flask import Blueprint

api = Blueprint('base_api',__name__)

from main_pack.api.errors import routes
from . import reg_no_api