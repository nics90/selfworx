#
# Cookbook:: selfworx_win_config
# Recipe:: restart_node
#
# Copyright:: 2019, The Authors, All Rights Reserved.

#Variables used in recipe
#reboot_reason = node[:selfworx_win_config][:restart_node][:reboot_justification]
reboot_reason = node[:reboot_justification]
delay         = node[:delay_win].to_i

#Reboot the server in 1 min
reboot 'now' do
  action :reboot_now
  reason "#{reboot_reason}"
  delay_mins delay
end
