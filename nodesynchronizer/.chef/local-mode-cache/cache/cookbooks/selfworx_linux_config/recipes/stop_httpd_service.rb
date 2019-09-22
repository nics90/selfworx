#
# Cookbook:: selfworx_linux_config
# Recipe:: stop_httpd_service
#
# Copyright:: 2019, The Authors, All Rights Reserved.

service 'httpd' do
  action :stop
end
