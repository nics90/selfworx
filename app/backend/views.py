from flask import Flask,render_template,redirect,request,url_for,session,jsonify,Response
from flask_login import login_required
from ..models import TargetGroup,TargetEnv,TargetNodeList,TargetGroupEnvNodeMapping,TargetRole,Task_Schedule,Job_Status,TargetSubActivity
from . import backend
from app import db
import json
from sqlalchemy import or_,and_
from crontab import CronTab
from datetime import datetime
from sqlalchemy import func

@backend.route('/addTargetGroup',methods=['GET','POST'])
def add_target_group():
  target_group_name = request.form['groupname']
  target_group_desc = request.form['groupdesc']
  if len(list(TargetGroup.query.filter_by(target_group_name=target_group_name))) != 0:
      data = {"redirect":"false","redirect_url":url_for('frontend.display_group')}
      return json.dumps(data)
  else:
      target_group_name_desc = TargetGroup(target_group_name,target_group_desc)
      db.session.add(target_group_name_desc)
      db.session.commit()
      data = {"redirect":"true","redirect_url":url_for('frontend.display_group')}
      return json.dumps(data)

@backend.route('/getGroup', methods=['GET','POST'])
def get_group():
    data = {}
    count = 0
    result = list(TargetGroup.query.all())
    for row in result:
      count = count + 1
      row = [row.target_group_name,row.target_group_desc]
      data.update({count:row})
    return json.dumps(data)

@backend.route('/addTargetEnv',methods=['GET','POST'])
def add_target_env():
  target_env_name = request.form['envname']
  target_env_desc = request.form['envdesc']
  if len(list(TargetEnv.query.filter_by(target_env_name=target_env_name))) != 0:
      data = {"redirect":"false","redirect_url":url_for('frontend.display_environment')}
      return json.dumps(data)
  else:
      target_env_name_desc = TargetEnv(target_env_name,target_env_desc)
      db.session.add(target_env_name_desc)
      db.session.commit()
      data = {"redirect":"true","redirect_url":url_for('frontend.display_environment')}
      return json.dumps(data)

@backend.route('/getEnvironment', methods=['GET','POST'])
def get_environment():
    data = {}
    count = 0
    result = list(TargetEnv.query.all())
    for row in result:
      count = count + 1
      row = [row.target_env_name,row.target_env_desc]
      data.update({count:row})
    return json.dumps(data)

@backend.route('/addTargetNodeList',methods=['GET','POST'])
def add_target_node_list():
  target_node_list = request.form['nodelist']
  target_node_type = request.form['nodetype']
  target_node_desc = request.form['nodedesc']
  if len(list(TargetNodeList.query.filter_by(target_node_list=target_node_list))) != 0:
      data = {"redirect":"false","redirect_url":url_for('frontend.display_node_list')}
      return json.dumps(data)
  else:
      target_node_list_desc = TargetNodeList(target_node_list,target_node_desc,target_node_type)
      db.session.add(target_node_list_desc)
      db.session.commit()
      data = {"redirect":"true","redirect_url":url_for('frontend.display_node_list')}
      return json.dumps(data)


@backend.route('/getNodeList', methods=['GET','POST'])
def get_node_list():
    data = {}
    count = 0
    result = list(TargetNodeList.query.all())
    for row in result:
      count = count + 1
      row = [row.target_node_list,row.target_node_type,row.target_node_desc]
      data.update({count:row})
    return json.dumps(data)

@backend.route('/addTargetGroupEnvNodeListMapping',methods=['GET','POST'])
def add_target_group_env_node_list_mapping():
  target_group_name = request.form['groupname']
  target_env_name = request.form['envname']
  target_node_list = request.form['nodelist']
  if len(list(TargetGroupEnvNodeMapping.query.filter(and_(TargetGroupEnvNodeMapping.target_group_name==target_group_name,TargetGroupEnvNodeMapping.target_env_name==target_env_name,TargetGroupEnvNodeMapping.target_node_list==target_node_list)))) != 0:
      data = {"redirect":"false","redirect_url":url_for('frontend.display_group_env_node_list_mapping')}
      return json.dumps(data)
  else:
      target_group_env_node_list = TargetGroupEnvNodeMapping(target_group_name,target_env_name,target_node_list)
      db.session.add(target_group_env_node_list)
      db.session.commit()
      data = {"redirect":"true","redirect_url":url_for('frontend.display_group_env_node_list_mapping')}
      return json.dumps(data)

@backend.route('/getTargetGroupEnvNode', methods=['GET','POST'])
def get_target_group_env_node():
    groupname = request.form['target_group']
    env = request.form['target_env']
    print("Selected",request.form['target_group'],request.form['target_env'])
    data = []
    target_group_env_node_list = list(TargetGroupEnvNodeMapping.query.filter(and_(TargetGroupEnvNodeMapping.target_group_name==groupname,TargetGroupEnvNodeMapping.target_env_name==env)))
    for target_group_env_node in target_group_env_node_list:
     # print(target_env.target_env_name)
      data.append({"target_group_name":target_group_env_node.target_group_name,"target_env_name":target_group_env_node.target_env_name,"target_node_list":target_group_env_node.target_node_list})
    print(data)
    return jsonify(result=data)

@backend.route('/getTargetGroup', methods=['GET','POST'])
def get_target_group():
    data = []
    target_group_list = list(TargetGroup.query.all())
    for target_group in target_group_list:
      print(target_group.target_group_name)
      data.append({"target_group_name":target_group.target_group_name})
    print(data)
    return jsonify(result=data)

@backend.route('/getTargetEnv', methods=['GET','POST'])
def get_target_env():
    data = []
    target_env_list = list(TargetEnv.query.all())
    for target_env in target_env_list:
      data.append({"target_env_name":target_env.target_env_name})
    return jsonify(result=data)

@backend.route('/getTargetNodeList', methods=['GET','POST'])
def get_target_node_list():
    data = []
    target_node_lists = list(TargetNodeList.query.all())
    for target_node_list in target_node_lists:
      data.append({"target_node_list":target_node_list.target_node_list})
    return jsonify(result=data)

@backend.route('/getGroupEnvNodeListMapping', methods=['GET','POST'])
def get_group_env_node_list_mapping():
    data = {}
    count = 0
    result = list(TargetGroupEnvNodeMapping.query.all())
    for row in result:
      count = count + 1
      row = [row.target_group_name,row.target_env_name,row.target_node_list]
      data.update({count:row})
    return json.dumps(data)

@backend.route('/getTargetRole', methods=['GET','POST'])
def get_target_role():
    data = []
    target_role_list = list(TargetRole.query.all())
    for target_role in target_role_list:
      print(target_role.target_role_name,target_role.target_role_display_name)
      data.append({"target_role_name":target_role.target_role_name,"target_role_display_name":target_role.target_role_display_name})
    print(data)
    return jsonify(result=data)

@backend.route('/getTime',methods=['GET'])
def get_time():
    def generate():
        yield datetime.now().strftime("%m/%d/%Y %H:%M:%S")  
    return Response(generate(), mimetype='text') 

@backend.route('/scheduleTask',methods=['POST'])
def schedule_task():
  target_group_name = request.form['target_group_name']
  target_env_name = request.form['target_env_name']
  target_node_list = request.form['target_node_list']
  target_role_name = request.form['target_role_name']
  task_scheduled_time = request.form['task_scheduled_time']
  task_status = 'Scheduled'
  if target_group_name != ''  and target_env_name != '' and target_node_list != '' and target_role_name != '' and task_scheduled_time !='':
      get_latest_task_id = db.session.query(func.max(Task_Schedule.task_id))
      latest_task_id = get_latest_task_id.one()[0]
      if latest_task_id is None:
          latest_task_id = 0
      task_id = latest_task_id + 1
      formatted_task_scheduled_time = datetime.strptime(task_scheduled_time, '%Y-%m-%dT%H:%M')
      task_scheduled_time = formatted_task_scheduled_time
      db.session.add(Task_Schedule(task_id,target_group_name,target_env_name,target_node_list,target_role_name,task_status,task_scheduled_time))
      db.session.commit()
      cron_task = CronTab(user='root')
      task = cron_task.new('sh /selfworx/scripts/task_executor.sh '+str(task_id))
      task.setall(task_scheduled_time)
      cron_task.write()
      data = {"redirect":"true","redirect_url":url_for('frontend.schedule_task')}
  else:
      data = {"redirect":"false","redirect_url":url_for('frontend.schedule_task')}
  return json.dumps(data)

@backend.route('/getScheduledTask', methods=['GET','POST'])
def get_scheduled_task():
    data = {}
    rows = []
    scheduled_task_list = list(Task_Schedule.query.all())
    for scheduled_task in scheduled_task_list:
       scheduled_task_data = {
	               'task_id' : scheduled_task.task_id,
		           'target_group_name' : scheduled_task.target_group_name,
		           'target_env_name' : scheduled_task.target_env_name,
		           'target_node_list' : scheduled_task.target_node_list,
	 	           'target_role_name' : scheduled_task.target_role_name,
		           'task_status' : scheduled_task.task_status,
		           'task_scheduled_time' : scheduled_task.task_scheduled_time.__str__()
	           }
       rows.append(scheduled_task_data)
    data.update({"data":rows})
    return json.dumps(data)

@backend.route('/getJobStatus', methods=['GET','POST'])
def get_job_status():
    data = {}
    rows = []
    job_status_list = list(Job_Status.query.all())
    for job_status in job_status_list:
       job_status_data = {
	               'job_id' : job_status.job_id,
		           'target_role_name' : job_status.target_role_name,
		           'target_node_name' : job_status.target_node_name,
	 	           'job_status' : job_status.job_status,
		           'job_created' : job_status.job_created.__str__(),
                   'job_updated' : job_status.job_updated.__str__(),
		           'task_id' : job_status.task_id
	           }
       rows.append(job_status_data)
    data.update({"data":rows})
    return json.dumps(data)

@backend.route('/getTargetSubActivity', methods=['GET','POST'])
def get_target_subactivity():
    data = []
    target_subactivity_list = list(TargetSubActivity.query.all())
    for target_subactivity in target_subactivity_list:
      print(target_subactivity.target_subactivity_name,target_subactivity.target_subactivity_display_name)
      data.append({"target_subactivity_name":target_subactivity.target_subactivity_name,"target_subactivity_display_name":target_subactivity.target_subactivity_display_name})
    print(data)
    return jsonify(data)

@backend.route('/getSelectedSubActivityListData', methods=['GET','POST'])
def get_selected_subactivity_list_data():
    selected_subactivity_list = request.form['selected_subactivity_list']
    selected_subactivities = selected_subactivity_list.split(',')
    #print(selected_runlist)
    subactivities_json_data = []
    for subactivity in selected_subactivities:
        subactivity_query = db.session.query(TargetSubActivity).filter(TargetSubActivity.target_subactivity_name == subactivity)
        result = db.session.execute(subactivity_query).fetchone()
        subactivities_json_data.append(result[2])
    return jsonify(subactivities_json_data)

@backend.route('/createActivity', methods=['GET','POST'])
def create_activity():
    activity = json.loads(request.form['activity'])
    print("*****************************")
    print(activity)
    print("*****************************")
    activity_name = activity['activity_name']
    activity_desc = activity['activity_desc']
    activity_data = []
    #activity_data.append(activity_name)
    #activity_data.append(activity_desc)
    #activity_data.append([])
    #print(activity['selected_sub_activites'])
    for sub_activity in activity['selected_sub_activites']:
        sub_activity_data = []
        sub_activity_name = sub_activity['name']
        sub_activity_attributes = sub_activity['default_attributes']
        role_query = db.session.query(TargetSubActivity).filter(TargetSubActivity.target_subactivity_name == sub_activity_name)
        result = db.session.execute(role_query).fetchone()
        #print("Target Sub Activity",result)
        sub_activity_json = json.loads(result[2])
        sub_activity_desc = sub_activity_json['description']
        sub_activity_run_list = sub_activity_json['run_list']
        #sub_activity = sub_activity_name+"|"+sub_activity_desc+"|"+sub_activity_attributes+"|"+sub_activity_run_list
        sub_activity_data.append(sub_activity_name)
        sub_activity_data.append(sub_activity_desc)
        sub_activity_data.append(sub_activity_attributes)
        sub_activity_data.append(sub_activity_run_list)
        #print(sub_activity_name,sub_activity_desc,sub_activity_attributes,sub_activity_run_list)
        print("-------------------------------")
        activity_data.append(sub_activity_data)
    print(activity_data)
    if len(list(TargetRole.query.filter_by(target_role_name=activity_name))) != 0:
        data = {"redirect":"false","redirect_url":url_for('frontend.drag_me')}
        return json.dumps(data)
    else:
        target_activity = TargetRole(activity_name,activity_name,activity_desc,str(activity_data))
        db.session.add(target_activity)
        db.session.commit()
        data = {"redirect":"true","redirect_url":url_for('frontend.schedule_task')}
        return json.dumps(data)
