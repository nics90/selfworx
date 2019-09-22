from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

activity_name = sys.argv[1]

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<name - {}>'.format(self.name)

class TargetGroup(Base):
    __tablename__ = "TargetGroup"
    target_group_name = Column(String(100), primary_key=True)
    target_group_desc = Column(String(250))

    def __init__(self, target_group_name, target_group_desc):
        self.target_group_name = target_group_name
        self.target_group_desc = target_group_desc

class TargetEnv(Base):
    __tablename__ = "TargetEnv"
    target_env_name = Column(String(100), primary_key=True)
    target_env_desc = Column(String(250))

    def __init__(self, target_env_name, target_env_desc):
        self.target_env_name = target_env_name
        self.target_env_desc = target_env_desc

class TargetNodeList(Base):
    __tablename__ = "TargetNodeList"
    target_node_list = Column(String(512), primary_key=True)
    target_node_desc = Column(String(250))
    target_node_type = Column(String(250))

    def __init__(self, target_node_list, target_node_desc,target_node_type):
        self.target_node_list = target_node_list
        self.target_node_desc = target_node_desc
        self.target_node_type = target_node_type

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
        self.target_role_desc = target_role_desc,
        self.target_role_data = target_role_data
        self.target_role_required_reboot = target_role_required_reboot


class TargetSubActivity(Base):
    __tablename__ = "TargetSubActivity"
    target_subactivity_name = Column(String(200), primary_key=True)
    target_subactivity_display_name = Column(String(250))
    target_subactivity_data = Column(Text)

    def __init__(self, target_subactivity_name, target_subactivity_display_name,target_subactivity_data):
        self.target_subactivity_name = target_subactivity_name
        self.target_subactivity_display_name = target_subactivity_display_name
        self.target_subactivity_data = target_subactivity_data

class TargetGroupEnvNodeMapping(Base):
    __tablename__ = "TargetGroupEnvNodeMapping"
    target_group_name = Column(String(100),ForeignKey('TargetGroup.target_group_name'),primary_key=True)
    target_env_name =  Column(String(100),ForeignKey('TargetEnv.target_env_name'),primary_key=True)
    target_node_list = Column(String(512),ForeignKey('TargetNodeList.target_node_list'))

    def __init__(self, target_group_name,target_env_name,target_node_list):
        self.target_group_name = target_group_name
        self.target_env_name = target_env_name
        self.target_node_list = target_node_list

class Task_Schedule(Base):
    __tablename__ = "Task_Schedule"
    task_id = Column(Integer, primary_key=True,autoincrement=True)
    target_group_name = Column(String(100),ForeignKey('TargetGroup.target_group_name'))
    target_env_name =  Column(String(100),ForeignKey('TargetEnv.target_env_name'))
    target_node_list = Column(String(512),ForeignKey('TargetNodeList.target_node_list'))
    target_role_name = Column(String(200),ForeignKey('TargetRole.target_role_name'))
    task_status = Column(String(200))
    task_scheduled_time = Column(DateTime)

    def __init__(self, task_id, target_group_name,target_env_name,target_node_list,target_role_name,task_status,task_scheduled_time):
        self.task_id = task_id
        self.target_group_name = target_group_name
        self.target_env_name = target_env_name
        self.target_node_list = target_node_list
        self.target_role_name = target_role_name
        self.task_status = task_status
        self.task_scheduled_time = task_scheduled_time

class Job_Status(Base):
    __tablename__ = "Job_Status"
    id = Column(Integer, primary_key=True,autoincrement=True)
    job_id = Column(Integer)
    target_role_name = Column(String(200))
    target_node_name = Column(String(200))
    job_status = Column(String(200))
    job_created = Column(DateTime)
    job_updated = Column(DateTime)
    task_id = task_id = Column(Integer,ForeignKey('Task_Schedule.task_id'))

    def __init__(self, job_id,target_role_name,target_node_name, job_status, job_created, job_updated, task_id):
        self.job_id = job_id
        self.target_node_name = target_node_name
        self.job_status = job_status
        self.target_role_name = target_role_name
        self.job_created = job_created
        self.job_updated = job_updated
        self.task_id = task_id

engine = create_engine('mysql://root:password@127.0.0.1/selfworx_app')
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
r = session.query(TargetRole).filter_by(target_role_name=activity_name).first()
print(r.target_role_data)
#for i in r:
    #print(i.target_role_data)
#tr = TargetRole.__table__
#print(tr)
#ab = tr.select()
#res = conn.execute(ab)
#for row in res:
#   print (row)
print(activity_name)
