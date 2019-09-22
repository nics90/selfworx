#
# Cookbook:: selfworx_win_config
# Recipe:: deploy_web_app_iis
#
# Copyright:: 2019, The Authors, All Rights Reserved.
# ----------------------------------------------------------------------------------
# This recipe assumes that the IIS is already installed on the server.
# If that is not the case, you should run "selfworx_win_config::install_iis" first.

#Get the global variables
ftp_7zip_url    = node[:selfworx_win_config][:deploy_web_app_iis][:ftp_7zip_url]
installer_7zip  = node[:selfworx_win_config][:deploy_web_app_iis][:installer_7zip]
exe_path_7z     = node[:selfworx_win_config][:deploy_web_app_iis][:install_path_7zip]
ftp_web_pkg_url = node[:selfworx_win_config][:deploy_web_app_iis][:ftp_web_pkg_url]
web_pkg_name_gz = node[:selfworx_win_config][:deploy_web_app_iis][:web_pkg_file]
web_pkg_tar     = web_pkg_name_gz.gsub(".gz","")
web_app_dir     = node[:selfworx_win_config][:deploy_web_app_iis][:web_install_path]
website_name    = node[:selfworx_win_config][:deploy_web_app_iis][:website_name_iis]
website_port    = node[:selfworx_win_config][:deploy_web_app_iis][:website_port_iis]

#Install 7-zip if not already present on the server
windows_package '7-Zip' do
    source "#{ftp_7zip_url}/#{installer_7zip}"
    installer_type :msi
end

#Download the website package from ftp Server
remote_file "#{Chef::Config[:file_cache_path]}/#{web_pkg_name_gz}" do
    source "#{ftp_web_pkg_url}/#{web_pkg_name_gz}"
    remote_user "ftpuser"
    remote_password "jmd@123"
    retries 3
end

#Create the Web App directory if not already present
directory "#{web_app_dir}" do
    action :create
    recursive true
end

#Extract the website to desired location
execute "Extract the files in #{web_pkg_tar} to #{web_app_dir}" do
    cwd "#{Chef::Config[:file_cache_path]}"
    command "\"#{exe_path_7z}\\7z.exe\" e #{web_pkg_name_gz} -y && \"#{exe_path_7z}\\7z.exe\" x #{web_pkg_tar} -o\"#{web_app_dir}\" -y"
end

#Host the website on IIS
powershell_script 'Create the website and Host it in IIS' do
    code <<-EOH
        $website_name = "#{website_name}"
        $website_port = "#{website_port}"
        $physical_path = "#{web_app_dir}"
        New-WebSite -Name $website_name -Port $website_port -PhysicalPath "$physical_path"
    EOH
end

#IISReset
execute 'IISReset' do
    command 'iisreset'
end 
