#!/bin/bash

#########  Set Initialization Variables Start ##########
task_id=$1
execution_dir='/selfworx/scripts/'
cd $execution_dir
log_dir=logs/task"$task_id"
data_dir=data/task"$task_id"
log_file_name="task_executor.log"
db_user=`grep 'db_user' config/task_config.ini | awk -F '=' '{print $2}'`
db_password=`grep 'db_password' config/task_config.ini | awk -F '=' '{print $2}'`
db_name=`grep 'db_name' config/task_config.ini | awk -F '=' '{print $2}'`
scheduled_task_data_file=`grep 'scheduled_task_data_file' config/task_config.ini | awk -F '=' '{print $2}'`
role_node_mapping_file=`grep 'role_node_mapping_file' config/task_config.ini | awk -F '=' '{print $2}'`
node_type_data_file=`grep 'node_type_data_file' config/task_config.ini | awk -F '=' '{print $2}'`
#########  Set Initialization Variables End  ##########

######### Delete Previous Log and Data Directories Start ########
rm -rf $log_dir
rm -rf $data_dir
rm -rf $data_dir/$role_node_mapping_file
######### Delete Previous Log and Data Directories End ##########

######### Create Previous Log and Data Directories Start ########
mkdir $log_dir
mkdir $data_dir
touch $data_dir/$role_node_mapping_file
######### Create Previous Log and Data Directories End ##########

if [ -z "$db_user" ] || [ -z "$db_password" ] || [ -z "$db_name" ] || [ -z "$scheduled_task_data_file" ] || [ -z "$role_node_mapping_file" ]; then
  echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Blank Value set in config file for any required configuration. Task execution failed." >$log_dir/$log_file_name
  sh update_task_status.sh $task_id "Failed"
  exit 1
else
  echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Initialization Variables set successfully." >$log_dir/$log_file_name
fi

######### Fetch Details of Task ID from Database Start ##########
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Fetching task details from database." >>$log_dir/$log_file_name
mysql -u$db_user -p$db_password $db_name <<EOF 1>$data_dir/$scheduled_task_data_file 2>>$log_dir/$log_file_name
select * from Task_Schedule where task_id="$task_id";
EOF
if [ `echo $?` -eq 0 ];then
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Successfully fetched task details from database." >>$log_dir/$log_file_name
else
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Failed to fetch task details from database." >>$log_dir/$log_file_name
fi
######### Fetch Details of Task ID from Database End ############

########  Fetch Role Name and Node List from Data file Start #####
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Fetching role name and node list from data file." >>$log_dir/$log_file_name
role_name=`awk '{print $5}' $data_dir/$scheduled_task_data_file | sed -n '2p'`
node_list=`awk '{print $4}' $data_dir/$scheduled_task_data_file | sed -n '2p'`

if [ -z "$role_name" ] || [ -z "$node_list" ]; then
  echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Either role Name or node list is blank. Task execution failed." >>$log_dir/$log_file_name
  sh update_task_status.sh $task_id "Failed"
  exit 1
else
  echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Successfully fetched role name and node list from data file." >>$log_dir/$log_file_name
fi

########  Fetch Role Name and Node List from Data file End #######

######### Create Role to Node Mapping from Data File Start #######
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Creating role to node mapping from data file." >>$log_dir/$log_file_name
IFS=';'
count=1
for node in $node_list
 do
   echo $count:"$role_name":"$node" >>$data_dir/$role_node_mapping_file
   count=$((count + 1))
 done
unset IFS
echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Finished creating role to node mapping from data file." >>$log_dir/$log_file_name
######### Create Role to Node Mapping from Data File End #########

######### Checking Node List Type Block Start ##########
mysql -u$db_user -p$db_password $db_name <<EOF 1>$data_dir/$node_type_data_file 2>>$log_dir/$log_file_name
select target_node_type from TargetNodeList LEFT JOIN TargetGroupEnvNodeMapping ON
TargetGroupEnvNodeMapping.target_node_list = TargetNodeList.target_node_list where TargetGroupEnvNodeMapping.target_node_list = "$node_list";
EOF
node_list_type=`sed -n '2p' $data_dir/$node_type_data_file`
######### Checking Node List Type Block End  ###########

######### Call Job Executor to Create and Execute Jobs Start #####

if [ "$node_list_type" = "linux" ]; then
  echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Passing the control over to linux job executor." >>$log_dir/$log_file_name
  sh -x job_executor_linux.sh $task_id
elif [ "$node_list_type" = "windows" ]; then
  echo "`date '+%Y-%m-%d %H:%M:%S'` :: <INFO> :: Passing the control over to windows job executor." >>$log_dir/$log_file_name
  sh job_executor.sh $task_id
else
  echo "`date '+%Y-%m-%d %H:%M:%S'` :: <ERROR> :: Unrecognized Node List Type. Hence, cannot continue." >>$log_dir/$log_file_name
fi
######### Call Job Executor to Create and Execute Jobs End #######
