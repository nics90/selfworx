#
# Cookbook:: selfworx_linux_config
# Recipe:: start_httpd_service
#
# Copyright:: 2019, The Authors, All Rights Reserved.

service 'httpd' do
  action :start
end
