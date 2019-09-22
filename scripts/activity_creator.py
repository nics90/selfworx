from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
import json
import shutil
##############################################################################################

Base = declarative_base()

class TargetRole(Base):
    __tablename__ = "TargetRole"
    target_role_name = Column(String(200), primary_key=True)
    target_role_display_name = Column(String(200), nullable=False)
    target_role_desc = Column(String(250))
    target_role_data = Column(Text)
    target_role_required_reboot = Column(Boolean, unique=False, nullable=False)

    def __init__(self, target_role_name, target_role_display_name,target_role_desc,target_role_data,target_role_required_reboot=False):
        self.target_role_name = target_role_name
        self.target_role_display_name = target_role_display_name
        self.target_role_desc = target_role_desc
        self.target_role_data = target_role_data
        self.target_role_required_reboot = target_role_required_reboot

##############################################################################################

activity_name = sys.argv[1]
engine = create_engine('mysql://root:password@127.0.0.1/selfworx_app')
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
row = session.query(TargetRole).filter_by(target_role_name=activity_name).first()
activity_name = row.target_role_name
activity_desc = row.target_role_desc
activity_data = eval(row.target_role_data)

os.chdir("roles/")
if os.path.exists(activity_name):
    os.system('rm -rf %s/*' % activity_name)
    os.rmdir(activity_name)

os.mkdir(activity_name)
os.chdir("../")

activity_path = "roles/"+ activity_name
activity_runlist = []
for subactivity in activity_data:
    subactivity_data = {
                        "name" : subactivity[0],
                        "description" : subactivity[1],
                        "default_attributes" : subactivity[2],
                        "run_list" : subactivity[3]
    }

    with open(activity_path+"/"+subactivity[0]+".json", 'w') as json_file:
        json.dump(subactivity_data, json_file,indent=4)
    activity_runlist.append("role["+subactivity[0]+"]")

activity_data = {
                 "name" : activity_name,
                 "description" : activity_desc,
                 "run_list" : activity_runlist
}
activity_json = json.dumps(activity_data, indent=4)

with open(activity_path+"/"+activity_name+".json", 'w') as activity_json_file:
    json.dump(activity_data, activity_json_file,indent=4)
