@echo off

rem Set the file path
echo Checking for old script...
set "file_path=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\htb-presence-startup.bat"

rem Check if the file exists
if exist "%file_path%" (
    rem File exists, so delete it
    del "%file_path%"
    echo Old startup script deleted.
)

rem Add Python script to startup
echo Adding new script to startup...
(
    echo :loop
    echo cd /d "%~dp0"
    echo python "%~dp0htb-presence.py"
    echo goto loop
) > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\htb-presence-startup.bat"
echo Done!