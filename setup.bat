@echo off

rem Set the file path
set "file_path=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\htb-presence-startup.bat"

rem Check if the file exists
if exist "%file_path%" (
    rem File exists, so delete it
    del "%file_path%"
    echo Old startup script deleted.
)

rem Add Python script to startup
echo :loop >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\htb-presence-startup.bat"
echo python "%~dp0htb-presence.py" >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\htb-presence-startup.bat"
echo goto loop >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\htb-presence-startup.bat"