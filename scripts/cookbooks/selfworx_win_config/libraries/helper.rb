require 'chef/application'
::Chef::Recipe.send(:include, Chef::Mixin::PowershellOut)

module Selfworx_Win_Config
    module Helper
        def getSystemUpTimeLocal()
            script = <<-EOH
			    Add-Type -Path '#{assemblyPath}'
			    $obj = New-Object Relsys.Common.General.Crypto
			    $result= $result=$obj.UserEncrypt('"#{password}"',[ref] 'error')
			    return $result
            EOH
            cmd = powershell_out(script)
            return cmd.stdout
        end

        def updateSystemUpTimeSelfworxApi()
        end

        def getSystemUpTimeSelfworxApi()
        end

        def successfulReboot()
        end

        def getWinTaskState(winTaskName)
            script = <<-EOH
			    $result = (Get-ScheduledTask | Where TaskName -eq "#{winTaskName}").State
			    return $result
            EOH
            cmd = powershell_out(script)
            return cmd.stdout
        end
    end
end