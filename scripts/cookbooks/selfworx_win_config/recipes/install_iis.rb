#
# Cookbook:: selfworx_win_config
# Recipe:: install_iis
#
# Copyright:: 2019, The Authors, All Rights Reserved.
# Install the required IIS components

#Install the IIS on web server 
powershell_script 'Install IIS' do
    code <<-EOH
        Import-Module ServerManager
        Install-WindowsFeature -Name Web-Server, Web-Mgmt-Tools
    EOH
end
  
#start the service
service "w3svc" do
    action [:enable,:start]
    ignore_failure true
    only_if    {::Win32::Service.exists?("w3svc")}
end
  
#start the service
service "IISADMIN" do
    action [:enable,:start]
    ignore_failure true
    only_if    {::Win32::Service.exists?("IISADMIN")}
end
  
#IISReset
execute 'IISReset' do
    command 'iisreset'
end  