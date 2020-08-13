from flask import Blueprint

bp = Blueprint('commerce_auth_test', __name__)

from main_pack.commerce_test.auth import (admin_auth)