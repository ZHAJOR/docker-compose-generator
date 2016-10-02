# Docker-compose-generator

## Required
-Docker  
-Docker-compose  
-Python3


## Before starting
The project goal is simple: winning time during the project initialization.
As developers we made APIs, fronts, databases ... every weeks.
Docker was amazing, allowed us to have various versions of sofwares (as php) without being a mess.
Then came docker-compose, we were able to run many containers with just a single command.
But the docker-compose.yml is annoying to write and 95% of time it's the same combo api, front, database.
It's why I decided to take care of this by writing a script. My first thought was a simple 'sed'. 
However it wasn't enough, imagine this time you just want a single database, possible but quite dirty.  
Here came docker-gen, you have to personalize the script for your usage.
At the beginning of the script you have a list of images available, feel free to add some.
Then came the default configuration of volumes, ports, envs... for api, front, db.  
You don't need to change anything else in the file.

## Usage
[MANDATORY] `--name my-project` the project name  
[MANDATORY] `--port 24000` the beginning port (it will be auto-incremented)  
[OPTIONAL]  `--file docker-compose.yml` the file to create default is docker-compose.yml  
[OPTIONAL]  `--no-front` do not create a front configuration  
[OPTIONAL]  `--no-api` do not create an api configuration  
[OPTIONAL]  `--no-db` do not create a db configuration  
[OPTIONAL]  `--no-db-admin` do not create a db administration configuration  
[OPTIONAL]  `--api phalcon` the image to use, need to be in the images available  
[OPTIONAL]  `--front phalcon` the image to use, need to be in the images available  
[OPTIONAL]  `--db phalcon` the image to use, need to be in the images available  
[OPTIONAL]  `--db-admin phalcon` the image to use, need to be in the images available  

If you do --no-db you do not need to add --no-db-admin.

## Example
`python3 docker-gen.py --name mylittle-project --port 5300 --no-front --no-db`  
It will create an api configuration with default (phalcon). Now just do :  
`docker-compose up -d`  
It's running ! With the default configuration the api directory is ./api and needs a public directory inside.


# Blog Article
Coming soon

## Conclusion
Have fun !
