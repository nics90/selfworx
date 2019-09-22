from flask import Blueprint
import os
#auth = Blueprint('auth', __name__)
#curr_dir=os.path.join(os.getcwd(),'app\\auth\\static')
#print(curr_dir)
auth = Blueprint('auth', __name__, template_folder='templates',static_folder='static')

from . import views
