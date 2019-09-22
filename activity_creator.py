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

#print(activity_name,activity_desc,activity_data)

if os.path.exists(activity_name):
    shutil.rmtree(activity_name, ignore_errors=True)
    os.rmdir(activity_name)

os.mkdir(activity_name)

activity_runlist = []
for subactivity in activity_data:
    subactivity_data = {
                        "name" : subactivity[0],
                        "description" : subactivity[1],
                        "default_attributes" : subactivity[2],
                        "run_list" : subactivity[3]
    }
    subactivity_json = json.dumps(subactivity_data, indent=4)
    print(subactivity_json)
    with open(activity_name+"/"+subactivity[0]+".json", 'w') as json_file:
        json.dump(subactivity_json, json_file,indent=4)
    activity_runlist.append("role["+subactivity[0]+"]")

activity_data = {
                 "name" : activity_name,
                 "description" : activity_desc,
                 "run_list" : activity_runlist
}
activity_json = json.dumps(activity_data, indent=4)
with open(activity_name+"/"+activity_name+".json", 'w') as activity_json_file:
    json.dump(activity_data, activity_json_file,indent=4)
#for i in r:
    #print(i.target_role_data)
#tr = TargetRole.__table__
#print(tr)
#ab = tr.select()
#res = conn.execute(ab)
#for row in res:
#   print (row)
print(activity_name)
