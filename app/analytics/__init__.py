from flask import Blueprint
import os

analytics = Blueprint('analytics', __name__, template_folder='templates',static_folder='static')
from . import views
