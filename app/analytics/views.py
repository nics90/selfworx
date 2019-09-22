from flask import Flask,render_template,redirect,request,url_for,session,jsonify
from flask_login import login_required
from ..models import TargetGroup,TargetEnv,TargetNodeList,TargetGroupEnvNodeMapping,TargetRole,Task_Schedule,Job_Status,TargetSubActivity
from . import analytics
from app import db
import json
from sqlalchemy import or_,and_
from crontab import CronTab
from datetime import datetime
from sqlalchemy import func

@analytics.route('/report1',methods=['GET'])
def buildReport1():
    data = TargetNodeList.query.with_entities(TargetNodeList.target_node_type, func.count(TargetNodeList.target_node_type)).group_by(TargetNodeList.target_node_type).all()
    labels_data = [ label[0] for label in data ] 
    values_data = [ value[1] for value in data ]
    total_count = sum(values_data) 
    data = {
        'labels':labels_data,
        'values':values_data,
	'server_count':total_count
    }
    return json.dumps(data)

@analytics.route('/report2',methods=['GET'])
def buildReport2():
    data = Task_Schedule.query.with_entities(Task_Schedule.task_status, func.count(Task_Schedule.task_status)).group_by(Task_Schedule.task_status).all()
    task_status = [ status[0] for status in data ] 
    values_data = [ value[1] for value in data ]
    total_count = sum(values_data) 
    data = {
        'task_status':task_status,
        'values':values_data,
	'tasks_count':total_count
    }
    return json.dumps(data)

@analytics.route('/report3',methods=['GET'])
def buildReport3():
    data = Job_Status.query.with_entities(Job_Status.job_status, func.count(Job_Status.job_status)).group_by(Job_Status.job_status).all()
    labels_data = [ label[0] for label in data ]
    values_data = [ value[1] for value in data ]
    total_count = sum(values_data)
    data = {
        'labels':labels_data,
        'values':values_data,
        'server_count':total_count
    }
    return json.dumps(data)

@analytics.route('/report4',methods=['GET'])
def buildReport4():
    data = Task_Schedule.query.with_entities(Task_Schedule.task_status, func.count(Task_Schedule.task_status)).group_by(Task_Schedule.task_status).all()
    labels_data = [ label[0] for label in data ]
    values_data = [ value[1] for value in data ]
    total_count = sum(values_data)
    data = {
        'labels':labels_data,
        'values':values_data,
        'server_count':total_count
    }
    return json.dumps(data)
