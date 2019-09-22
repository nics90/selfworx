from flask import render_template
from flask_login import login_required

from . import frontend


@login_required
@frontend.route('/dashboard',methods=['GET','POST'])
def dashboard():
  return render_template('dashboard.html')

@frontend.route('/addGroup',methods=['GET','POST'])
def add_group():
  return render_template('AddGroup.html')

@frontend.route('/displayGroup',methods=['GET','POST'])
def display_group():
  return render_template('DisplayGroup.html')

@frontend.route('/addEnvironment',methods=['GET','POST'])
def add_environment():
  return render_template('AddEnvironment.html')

@frontend.route('/displayEnvironment',methods=['GET','POST'])
def display_environment():
  return render_template('DisplayEnvironment.html')

@frontend.route('/addNodeList',methods=['GET','POST'])
def add_node_list():
  return render_template('AddNodeList.html')

@frontend.route('/displayNodeList',methods=['GET','POST'])
def display_node_list():
  return render_template('DisplayNodeList.html')

@frontend.route('/addGroupEnvNodeListMapping',methods=['GET','POST'])
def add_group_env_node_list_mapping():
  return render_template('AddMapping.html')

@frontend.route('/displayGroupEnvNodeListMapping',methods=['GET','POST'])
def display_group_env_node_list_mapping():
  return render_template('DisplayMapping.html')

@frontend.route('/scheduleTask',methods=['GET','POST'])
def schedule_task():
  return render_template('ScheduleTask.html')

@frontend.route('/getscheduleTasks',methods=['GET','POST'])
def get_scheduled_tasks():
  return render_template('TaskScheduled.html')

@frontend.route('/jobStatus',methods=['GET','POST'])
def job_status():
  return render_template('JobStatus.html')

@frontend.route('/createActivity',methods=['GET'])
def create_activity():
  return render_template('CreateActivity.html')
