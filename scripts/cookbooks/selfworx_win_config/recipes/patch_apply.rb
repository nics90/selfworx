#
# Cookbook:: selfworx_win_config
# Recipe:: patch_apply
#
# Copyright:: 2019, The Authors, All Rights Reserved.
require 'chef/application'
::Chef::Recipe.send(:include, Selfworx_Win_Config::Helper)


#Get the patch list and other global variables.
#patches             = node[:selfworx_win_config][:patch_apply][:patch_list]
patches = node[:patch_list].split(",")
patch_remote_loc = node[:ftp_patch_url]
#patch_remote_loc    = node[:selfworx_win_config][:patch_apply][:ftp_patch_url]
logPath             = node[:selfworx_win_config][:patch_apply][:execution_log_path]
#winTaskName         = node[:selfworx_win_config][:patch_apply][:win_task_name]
winTaskName         = "Patch Apply"
hostName            = node[:fqdn]
node.default['selfworx_win_config']['patch_list_script'] = ''
#patch_list_script   = ''
username="ftpuser"
password="jmd@123"

#Create a directory for log of patch apply
directory "#{logPath}" do
    action :create
    recursive true
end

#Loop through the list to Download the patches and create a list for powershell.
patches.each do |patch|
    Chef::Log.info "Downloading patch #{patch}"
    #Download the patch from ftp server
    remote_file "#{Chef::Config[:file_cache_path]}/#{patch}" do
        source "#{patch_remote_loc}/#{patch}"
	    remote_user "anonymous"
	    remote_password ""
        retries 3
    end
#Create a list to be used by powershell
  ruby_block "Create List" do
    block do
    if node['selfworx_win_config']['patch_list_script'].empty?
        node.default['selfworx_win_config']['patch_list_script'] = "\"" + "#{Chef::Config[:file_cache_path]}/#{patch}" + "\""
Chef::Log.info "--------------- Patch List #{node['selfworx_win_config']['patch_list_script']} ------------------"
    else
        node.default['selfworx_win_config']['patch_list_script'] = patch_list_script + ", " + "\"" + "#{Chef::Config[:file_cache_path]}/#{patch}" + "\""
Chef::Log.info "---------------else Patch List #{node['selfworx_win_config']['patch_list_script']} ------------------"
    end
    end
   end
end
Chef::Log.info "---------------outer Patch List #{node['selfworx_win_config']['patch_list_script']} ------------------"
#Create the powershell file from template
=begin
template "#{Chef::Config[:file_cache_path]}\\patchApply.ps1" do 
source "patchApply.ps1.erb"	
variables ({
	:patchList => node['selfworx_win_config']['patch_list_script']
      })
sensitive true
end
=end
ruby_block 'Create Template' do
 action :create
  block do
    r = Chef::Resource::Template.new("#{Chef::Config[:file_cache_path]}\\patchApply.ps1",run_context)
    r.source "patchApply.ps1.erb"
    r.cookbook 'selfworx_win_config'
    r.variables ({
       :patchList => node['selfworx_win_config']['patch_list_script']
    })
    r.run_action :create
  end
end
#Create and Run a windows task to apply patches
windows_task "#{winTaskName}" do
  command "Powershell.exe -File #{Chef::Config[:file_cache_path]}\\patchApply.ps1"
  run_level :highest
  frequency :none
  action [:create, :run]
end 

#Sync-Up time to get the task created and enter in running state
ruby_block 'Waiting for the task to start' do
    block do
        sleep 10
    end
end
=begin
#Get the initial State of task
winTaskState = getWinTaskState("#{winTaskName}")
timeLapsed = 10

#Hold on until the task has finished
until winTaskState == "Ready" do
    Chef::Log.info "#{winTaskName} task is in '#{winTaskState}' state since #{timeLapsed} seconds."
    ruby_block 'Syncing up task state' do
        block do
            sleep 30
        end
    end
    timeLapsed = timeLapsed + 30
    winTaskState = getWinTaskState("#{winTaskName}")
    if winTaskState == "Ready" then
        Chef::Log.info "#{winTaskName} task has completed in #{timeLapsed} seconds."
    end
end
=end
