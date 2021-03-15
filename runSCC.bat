@echo off

set nameProperty=project.name
set pathProperty=project.path
set languagesProperty=project.lang

set projectName=unnamed

if not exist "project.properties" (
    echo No project.properties file found
    echo Created project.properties file
    echo Please fill the file with the properties of the project you want to analyze
    copy NUL project.properties > NUL
    pause
    exit /b 1
)

rem at this point the project.properties file should exist

rem search for project.name property
findstr "project.name=" project.properties > NUL
if %ERRORLEVEL% EQU 0 (
    for /F "tokens=2 delims==" %%a in ('findstr /I "project.name=" project.properties') do set "projectName=%%a"  
)

rem search for project.path property
findstr "project.path=" project.properties > NUL
if %ERRORLEVEL% EQU 0 (
    for /F "tokens=2 delims==" %%a in ('findstr /I "project.path=" project.properties') do set "projectPats=%%a"  
) else (
    echo You must add the project path using the project.path property
    echo Add project.path in project.properties
    pause
    exit /b 2
)

if not exist %projectPats% (
    echo Project path not valid
    pause
    exit /b 3
)

if not exist tmp (
    mkdir tmp
)

if not exist out (
    mkdir out
)

rem at this point project path and project name should be stored
rem call scc
bin\win\scc.exe -f json -o tmp/%projectName%-raw.json --by-file %projectPats% > NUL
pushd src
python main.py
popd src
rmdir /s /q tmp

echo Analysis finished. Check out directory for %projectName%-results.json
pause
