#Variables used in restart_node recipe
default[:selfworx_win_config][:restart_node][:reboot_justification] = "Restarting the node post patch installation"

#Variables used in patch_apply recipe
default[:selfworx_win_config][:patch_apply][:patch_list]         = ["Windows8.1-KB4499151-x64.msu"]
default[:selfworx_win_config][:patch_apply][:ftp_patch_url]      = "ftp://1.1.1.71/pub"
default[:selfworx_win_config][:patch_apply][:execution_log_path] = "C:/Temp/PatchInstall/logs"
default[:selfworx_win_config][:patch_apply][:win_task_name]      = "PatchApply-Selfworx"

#Variables used in deploy_web_app_iis recipe
default[:selfworx_win_config][:deploy_web_app_iis][:ftp_7zip_url]      = "ftp://1.1.1.71/pub"
default[:selfworx_win_config][:deploy_web_app_iis][:installer_7zip]    = "7z1900-x64.msi"
default[:selfworx_win_config][:deploy_web_app_iis][:install_path_7zip] = "C:\\Program Files\\7-Zip"
default[:selfworx_win_config][:deploy_web_app_iis][:ftp_web_pkg_url]   = "ftp://1.1.1.71/pub"
default[:selfworx_win_config][:deploy_web_app_iis][:web_pkg_file]      = "webapp.tar.gz"
default[:selfworx_win_config][:deploy_web_app_iis][:website_name_iis]  = "Startup"
default[:selfworx_win_config][:deploy_web_app_iis][:website_port_iis]  = "8080"
default[:selfworx_win_config][:deploy_web_app_iis][:web_install_path]  = "C:\\Program Files\\WebApp"