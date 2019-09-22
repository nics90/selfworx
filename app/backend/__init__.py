from flask import Blueprint
import os
#curr_dir=os.path.join(os.getcwd(),'app\\home\\static')
#print(curr_dir)
#home = Blueprint('home', __name__)
#home = Blueprint('home', __name__, template_folder='templates',static_folder="D:\\JMD\\final\\app\\home\\static")
backend= Blueprint('backend', __name__, template_folder='templates',static_folder='static')
from . import views
