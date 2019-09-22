from app import db, login_manager
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)

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

class TargetGroup(db.Model):
    __tablename__ = "TargetGroup"
    target_group_name = db.Column(db.String(100), primary_key=True)
    target_group_desc = db.Column(db.String(250))

    def __init__(self, target_group_name, target_group_desc):
        self.target_group_name = target_group_name
        self.target_group_desc = target_group_desc

class TargetEnv(db.Model):
    __tablename__ = "TargetEnv"
    target_env_name = db.Column(db.String(100), primary_key=True)
    target_env_desc = db.Column(db.String(250))

    def __init__(self, target_env_name, target_env_desc):
        self.target_env_name = target_env_name
        self.target_env_desc = target_env_desc

class TargetNodeList(db.Model):
    __tablename__ = "TargetNodeList"
    target_node_list = db.Column(db.String(512), primary_key=True)
    target_node_desc = db.Column(db.String(250))
    target_node_type = db.Column(db.String(250))

    def __init__(self, target_node_list, target_node_desc,target_node_type):
        self.target_node_list = target_node_list
        self.target_node_desc = target_node_desc
        self.target_node_type = target_node_type

class TargetRole(db.Model):
    __tablename__ = "TargetRole"
    target_role_name = db.Column(db.String(200), primary_key=True)
    target_role_display_name = db.Column(db.String(200), nullable=False)
    target_role_desc = db.Column(db.String(250))
    target_role_data = db.Column(db.Text)
    target_role_required_reboot = db.Column(db.Boolean, unique=False, nullable=False)

    def __init__(self, target_role_name, target_role_display_name,target_role_desc,target_role_data,target_role_required_reboot=False):
        self.target_role_name = target_role_name
        self.target_role_display_name = target_role_display_name
        self.target_role_desc = target_role_desc,
        self.target_role_data = target_role_data
        self.target_role_required_reboot = target_role_required_reboot


class TargetSubActivity(db.Model):
    __tablename__ = "TargetSubActivity"
    target_subactivity_name = db.Column(db.String(200), primary_key=True)
    target_subactivity_display_name = db.Column(db.String(250))
    target_subactivity_data = db.Column(db.Text)

    def __init__(self, target_subactivity_name, target_subactivity_display_name,target_subactivity_data):
        self.target_subactivity_name = target_subactivity_name
        self.target_subactivity_display_name = target_subactivity_display_name
        self.target_subactivity_data = target_subactivity_data

class TargetGroupEnvNodeMapping(db.Model):
    __tablename__ = "TargetGroupEnvNodeMapping"
    target_group_name = db.Column(db.String(100),db.ForeignKey('TargetGroup.target_group_name'),primary_key=True)
    target_env_name =  db.Column(db.String(100),db.ForeignKey('TargetEnv.target_env_name'),primary_key=True)
    target_node_list = db.Column(db.String(512),db.ForeignKey('TargetNodeList.target_node_list'))

    def __init__(self, target_group_name,target_env_name,target_node_list):
        self.target_group_name = target_group_name
        self.target_env_name = target_env_name
        self.target_node_list = target_node_list

class Task_Schedule(db.Model):
    __tablename__ = "Task_Schedule"
    task_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    target_group_name = db.Column(db.String(100),db.ForeignKey('TargetGroup.target_group_name'))
    target_env_name =  db.Column(db.String(100),db.ForeignKey('TargetEnv.target_env_name'))
    target_node_list = db.Column(db.String(512),db.ForeignKey('TargetNodeList.target_node_list'))
    target_role_name = db.Column(db.String(200),db.ForeignKey('TargetRole.target_role_name'))
    task_status = db.Column(db.String(200))
    task_scheduled_time = db.Column(db.DateTime)

    def __init__(self, task_id, target_group_name,target_env_name,target_node_list,target_role_name,task_status,task_scheduled_time):
        self.task_id = task_id
        self.target_group_name = target_group_name
        self.target_env_name = target_env_name
        self.target_node_list = target_node_list
        self.target_role_name = target_role_name
        self.task_status = task_status
        self.task_scheduled_time = task_scheduled_time

class Job_Status(db.Model):
    __tablename__ = "Job_Status"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    job_id = db.Column(db.Integer)
    target_role_name = db.Column(db.String(200))
    target_node_name = db.Column(db.String(200))
    job_status = db.Column(db.String(200))
    job_created = db.Column(db.DateTime)
    job_updated = db.Column(db.DateTime)
    task_id = task_id = db.Column(db.Integer,db.ForeignKey('Task_Schedule.task_id'))

    def __init__(self, job_id,target_role_name,target_node_name, job_status, job_created, job_updated, task_id):
        self.job_id = job_id
        self.target_node_name = target_node_name
        self.job_status = job_status
        self.target_role_name = target_role_name
        self.job_created = job_created
        self.job_updated = job_updated
        self.task_id = task_id
