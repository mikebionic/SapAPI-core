from flask import Blueprint

bp = Blueprint('models_test', __name__)

from .base import models as base_models
from .commerce import models as commerce_models
from .hr_department import models as hr_department_models
from .users import models as users_models