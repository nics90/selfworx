#!/bin/bash

#########  Set Initialization Variables Start  ##########
task_id=$1
task_status=$2
execution_dir='/selfworx/scripts/'
cd $execution_dir
log_dir=logs/task"$task_id"
data_dir=data/task"$task_id"
log_file_name="task_executor.log"
db_user=`grep 'db_user' config/task_config.ini | awk -F '=' '{print $2}'`
db_password=`grep 'db_password' config/task_config.ini | awk -F '=' '{print $2}'`
db_name=`grep 'db_name' config/task_config.ini | awk -F '=' '{print $2}'`

#########  Set Initialization Variables End  ##########

mysql -u$db_user -p$db_password $db_name <<EOF 2>>$log_dir/$log_file_name
update Task_Schedule set task_status="$task_status" where task_id="$task_id";
EOF

if [ `echo $?` -eq 0 ];then
exit 0
else
exit 1
fi
