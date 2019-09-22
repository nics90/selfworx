import json
from models import TargetRole
#from app import db
with open('../roles/config_linux_reboot.json') as json_file:
    data = json.load(json_file)
    print(data)
    print(TargetRole.query.all())
