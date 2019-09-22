#!/bin/bash

#########  Set Initialization Variables Start ##########
task_id=$1
execution_dir='/selfworx/scripts/'
cd $execution_dir
log_dir=logs/task"$task_id"
data_dir=data/task"$task_id"
log_file_name="task_executor.log"
role_node_mapping_file=`grep 'role_node_mapping_file' config/task_config.ini | awk -F '=' '{print $2}'`
roles_json_path=`grep 'roles_json_path' config/task_config.ini | awk -F '=' '{print $2}'`
db_user=`grep 'db_user' config/task_config.ini | awk -F '=' '{print $2}'`
db_password=`grep 'db_password' config/task_config.ini | awk -F '=' '{print $2}'`
db_name=`grep 'db_name' config/task_config.ini | awk -F '=' '{print $2}'`
linux_execution_user=`grep 'linux_execution_user' config/task_config.ini | awk -F '=' '{print $2}'`
linux_execution_password=`grep 'linux_execution_password' config/task_config.ini | awk -F '=' '{print $2}'`
#########  Set Initialization Variables End  ##########
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Initialization Variables set successfully in Job Executor." >>$log_dir/$log_file_name

#########  Set Task Status Running in Database Start  ##########
sh update_task_status.sh $task_id "Running"
if [ `echo $?` -eq 0 ];then
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Task Status successfully marked 'Running' in database." >>$log_dir/$log_file_name
else
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Failed to mark task status in database." >>$log_dir/$log_file_name
exit 1
fi
#########  Set Task Status Running in Database End    ##########

#########  Set Initialization Variables End  ##########
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Traversing jobs from role to node mapping file." >>$log_dir/$log_file_name
for row in `cat $data_dir/$role_node_mapping_file`
 do
  job_id=`echo $row | awk -F':' '{print $1}'`
  role_name=`echo $row | awk -F':' '{print $2}'`
  node_name=`echo $row | awk -F':' '{print $3}'`
  if [ -z "$job_id" ] || [ -z "$role_name" ] || [ -z "$node_name" ]; then
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Either job id, role name or node name is blank. Task execution failed." >>$log_dir/$log_file_name
    sh update_task_status.sh $task_id "Failed"
    if [ `echo $?` -eq 0 ];then
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Task Status successfully marked 'Failed' in database." >>$log_dir/$log_file_name
    exit 1
    else
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Failed to mark task status in database." >>$log_dir/$log_file_name
    exit 1
    fi
  else
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Successfully fetched job id, role name or node name from role to node mapping file." >>$log_dir/$log_file_name
  fi
  #########  Create Job in database Start ##########
  TIMESTAMP=`date +'%Y-%m-%d %H:%M:%S'`
  mysql -u$db_user -p$db_password $db_name <<EOF 2>>$log_dir/$log_file_name
  insert into Job_Status (job_id,target_role_name,target_node_name,job_status,job_created,job_updated,task_id) VALUES ("$job_id","$role_name","$node_name","Created","$TIMESTAMP","$TIMESTAMP","$task_id");
EOF
  if [ `echo $?` -eq 0 ];then
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Successfully created job with Job ID: $job_id in database." >>$log_dir/$log_file_name
  else
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Failed to create job with JOB ID: $job_id in database." >>$log_dir/$log_file_name
    exit 1
  fi
#########  Create Job in database End ##########

###### Upload Roles on Chef Server Start ########
pwd
/opt/rh/rh-python36/root/usr/bin/python3 activity_creator.py $role_name
sleep 5
if [ -d "$roles_json_path"/"$role_name" ];then
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Successfully found activity directory." >>$log_dir/$log_file_name
    for file in "$roles_json_path"/"$role_name"/*
     do
       knife role from file $file
     done
else
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Failed to find activity directory." >>$log_dir/$log_file_name
    exit 1
fi

###### Upload Roles on Chef Server End  #########

######### Job Execution Block Start  ############
  echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Job ID: $job_id : Executing Role $role_name on Node $node_name." >>$log_dir/$log_file_name
  TIMESTAMP=`date +'%Y-%m-%d %H:%M:%S'`
  mysql -u$db_user -p$db_password $db_name <<EOF 2>>$log_dir/$log_file_name
  update Job_Status set job_status="Executing",job_updated="$TIMESTAMP" where (job_id="$job_id" and task_id="$task_id");
EOF
  if [ `echo $?` -eq 0 ];then
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Successfully updated job status 'Executing' with Job ID: $job_id in database." >>$log_dir/$log_file_name
  else
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Failed to mark job status 'Executing' with JOB ID: $job_id in database." >>$log_dir/$log_file_name
    exit 1
  fi
  #################################
  for role in $(ls "roles/$role_name/") 
  do
    if [ "$role" = "linux_server_reboot.json" ];then
      exit_code_on_success=35
      break
   else
     exit_code_on_success=0
   fi
  done
  echo "Code $exit_code_on_success"
 # if [ "$role_name" = "config_linux_reboot" ];then
 #    exit_code_on_success=35
 #  else
 #    exit_code_on_success=0
 #  fi
  knife ssh -m $node_name "chef-client -r 'role[$role_name]' -l info --once" -x "$linux_execution_user" -P "$linux_execution_password" >>$log_dir/$log_file_name
  if [ `echo $?` -eq $exit_code_on_success ];then
   echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Job ID: $job_id : Successfully executed Role $role_name on Node $node_name." >>$log_dir/$log_file_name
   TIMESTAMP=`date +'%Y-%m-%d %H:%M:%S'`
   mysql -u$db_user -p$db_password $db_name <<EOF 2>>$log_dir/$log_file_name
   update Job_Status set job_status="Completed",job_updated="$TIMESTAMP" where (job_id="$job_id" and task_id="$task_id");
EOF
   if [ `echo $?` -eq 0 ];then
     echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Successfully updated job status 'Completed' with Job ID: $job_id in database." >>$log_dir/$log_file_name
   else
     echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Failed to mark job status 'Completed' with JOB ID: $job_id in database." >>$log_dir/$log_file_name
     exit 1
   fi
  else
   echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Job ID: $job_id : Failed to execute Role $role_name on Node $node_name." >>$log_dir/$log_file_name
   TIMESTAMP=`date +'%Y-%m-%d %H:%M:%S'`
   mysql -u$db_user -p$db_password $db_name <<EOF 2>>$log_dir/$log_file_name
   update Job_Status set job_status="Failed",job_updated="$TIMESTAMP" where (job_id="$job_id" and task_id="$task_id");
EOF
   if [ `echo $?` -eq 0 ];then
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Successfully updated job status 'Failed' with Job ID: $job_id in database." >>$log_dir/$log_file_name
   else
    echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Failed to mark job status 'Failed' with JOB ID: $job_id in database." >>$log_dir/$log_file_name
    exit 1
   fi
  fi
  #################################
 done


#########  Set Task Status Finished in Database Start  ##########
sh update_task_status.sh $task_id "Finished"
if [ `echo $?` -eq 0 ];then
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Task Status successfully marked 'Finished' in database." >>$log_dir/$log_file_name
else
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Failed to mark task status in database." >>$log_dir/$log_file_name
exit 1
fi
#########  Set Task Status Finished in Database End    ##########
