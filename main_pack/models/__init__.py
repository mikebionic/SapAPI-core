from flask import Blueprint

bp = Blueprint('models', __name__)

from .base import models as base_models
from .commerce import models as commerce_models
from .hr_department import models as hr_department_models
from .users import models as users_models