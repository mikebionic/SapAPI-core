from flask import Blueprint

bp = Blueprint('base', __name__)

from main_pack.base import num2text
from .get_first_from_list import get_first_from_list
from .get_id_from_list_indexing import get_id_from_list_indexing