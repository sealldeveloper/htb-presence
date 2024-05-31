@echo off
rem Add Python script to startup
echo pythonw "%~dp0htb-presence.py" >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\htb-presence-startup.bat"

@REM @echo off
@REM rem Create a VBScript to launch Python script invisibly
@REM echo Set objShell = CreateObject("WScript.Shell") > "%TEMP%\RunPythonScript.vbs"
@REM echo objShell.Run "pythonw ""%~dp0htb-presence.py""", 0, False >> "%TEMP%\RunPythonScript.vbs"

@REM rem Add VBScript to startup
@REM move /y "%TEMP%\RunPythonScript.vbs" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\"

@REM rem Clean up temporary VBScript file
@REM del "%TEMP%\RunPythonScript.vbs"
