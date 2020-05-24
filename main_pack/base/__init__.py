from flask import Blueprint

bp = Blueprint('base', __name__)

from main_pack.base import num2text