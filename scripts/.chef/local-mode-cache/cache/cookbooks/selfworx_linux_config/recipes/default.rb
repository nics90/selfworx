#
# Cookbook:: selfworx_linux_config
# Recipe:: default
#
# Copyright:: 2019, The Authors, All Rights Reserved.

include_recipe "selfworx_linux_config::install_httpd"
include_recipe "selfworx_linux_config::stop_httpd_service"
include_recipe "selfworx_linux_config::start_httpd_service"
