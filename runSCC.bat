@echo off

set nameProperty=project.name
set pathProperty=project.path
set languagesProperty=project.lang

set projectName=unnamed
set projectPats=""

if not exist cfg (
    echo No cfg directory found
    echo Created cfg directory
    mkdir cfg
)

if not exist cfg\project.properties (
    echo No project.properties file found
    echo Created project.properties file
    echo Please fill the file with the properties of the project you want to analyze
    pushd cfg
    copy NUL project.properties > NUL
    popd
    pause
    exit /b 1
)

rem at this point the project.properties file should exist

rem search for project.name property
findstr "project.name=" cfg\project.properties > NUL
if %ERRORLEVEL% EQU 0 (
    for /F "tokens=2 delims==" %%a in ('findstr /I "project.name=" cfg\project.properties') do set "projectName=%%a"
    if "%projectName%" == "" (
        projectName = unnamed
    )
)

rem search for project.path property
findstr "project.path=" cfg\project.properties > NUL
if %ERRORLEVEL% EQU 0 (
    for /F "tokens=2 delims==" %%a in ('findstr /I "project.path=" cfg\project.properties') do set "projectPats=%%a"
) else (
    echo You must add the project path using the project.path property
    echo Add project.path in project.properties
    pause
    exit /b 2
)

if "%projectPats%" == "" (
    echo Add project.path in project.properties
    pause
    exit /b 3
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
