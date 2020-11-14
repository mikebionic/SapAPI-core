from flask import Blueprint

api = Blueprint('base_api',__name__)

from . import reg_no_api