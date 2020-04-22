from flask import Blueprint

bp = Blueprint('main', __name__)

from main_pack.main import routes