# SCC wrapper for DX-platform
SCC-wrapper is a plugin that uses the [SCC static analysis](https://github.com/boyter/scc) tool and converts its output into a DX-platform accepted format.

## Needed tools
Python 3.x

## Installation
This plugin can be cloned straight from Github

- via HTTPS

```
git clone https://github.com/luigibolovan/ces-qa-plugin.git
```

- via SSH

```
git clone git@github.com:luigibolovan/ces-qa-plugin.git
```

and is also available on Dockerhub

```
docker pull luigibolovan/scc-wrapper:1.0.1
```

## Getting started

### Project configuration
In order to have your project analyzed and prepared for DX integration, you need to fill the ```project.properties``` file from the ```cfg``` directory with the project name, the path of the project on your machine and a list of languages used for filtering only the files that have an extension associated with the specified languages.

The project name and the list of languages are not mandatory.

If the project name is missing, the output file will be ```unnamed-results.json```, otherwise the output file will be ```${project.name}-results.json```

If the list of languages is not specified, the results will not be filtered.

The provided languages are verified if they exist in the list of scc recognized languages(located in *data* directory). If one of the provided languages does not exist, it will be ignored.

#### Project properties file syntax
```python
project.name=${name of the project}
project.path=${absolute path of the project}
project.lang=${list of languages - comma separated only}
```

### Running the tool
The tool can be run on both Unix and Windows based operating systems.

For Unix

```shell
bash runSCC.sh
```

For Windows

```batch
runSCC.bat
```
The scripts will generate a json file in the ```out``` directory based on the properties set in ```project.properties``` .

#### Running using docker

```docker
docker run -v ${path to directory containing project.properties file}:/sccwrapper/cfg
           -v ${path to directory where the output will be generated}:/sccwrapper/out
           -v ${project.path value}:${project.path value}
           luigibolovan/scc-wrapper
```

## Output file format
The output json file will have the following format:

```javascript
[
  ...
  
   {
       "name": "${property}",
       "category": "SCC",
       "file": "${file-path}",
       "value": ${value-of-the-property}
   }
   
  ...
]
```

```property``` can be equal with *Blank*, *Code*, *Comment*

```file-path``` will be relative to project root

## Integration with DX-Platform
The output file will be uploaded as a properties file for the analyzed project in DX-Platform.

After uploading the properties file, the results will appear on the project's system map.

Example for Apache Kafka analysis:
![kafka-example](demo/demo-scc-wrapper-6.gif)

## Acknowledgements
This plugin relies on the [SCC static analysis](https://github.com/boyter/scc) concepts. Its binaries are included in the ```bin``` folder of the project. 
