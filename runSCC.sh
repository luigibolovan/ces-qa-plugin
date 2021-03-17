#!/bin/bash

nameProperty="project.name"
pathProperty="project.path"
languagesProperty="project.lang"

projectName="unnamed"

if [ ! -d cfg ]; then
    echo "No cfg directory found"
    echo "Created cfg directory"
    mkdir cfg
fi

if [ ! -f cfg/project.properties ]; then
    echo "No project.properties file found."
    echo "Created project.properties file"
    echo "Please fill the file with the properties of the project you want to analyze"
    pushd cfg > /dev/null
    touch project.properties
    popd > /dev/null
    exit 1
fi

# at this point the project.properties should exist

# search for project.name property
grep $nameProperty cfg/project.properties > /dev/null
if [ $? -eq 0 ]; then
    projectName=`grep -o "$nameProperty.*" cfg/project.properties | cut -f 2- -d= | cut -d ' ' -f 2`
fi

# search for project.path property
grep $pathProperty cfg/project.properties > /dev/null
if [ $? -eq 0 ]; then
    projectPath=`grep -o "$pathProperty.*" cfg/project.properties | cut -f 2- -d= | cut -d ' ' -f 2`
else
    echo "You must add the project path using the project.path property"
    echo "Add project.path in project.properties"
    exit 2
fi

if [ ! -d $projectPath ]; then
    echo "Project path not valid"
    exit 3
fi

if [ ! -d tmp/ ]; then
    mkdir tmp
fi

if [ ! -d out/ ]; then
    mkdir out
fi

# at this point project path and project name should be stored
# call scc
./bin/unix/scc -f json -o tmp/${projectName}-raw.json --by-file $projectPath > /dev/null

pushd src > /dev/null
python3 main.py
popd > /dev/null
rm -rf tmp

echo "Analysis finished. Check out directory for ${projectName}-results.json"
