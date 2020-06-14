# README
This folder contains all the necessary folders which is used by the deploy
script (start.sh).

Modify setup.yml to your liking here.

## docker_challenges
This folder contains all the folders with content to create docker containers
for hosting challenges.   
A docker-compose.yml is needed to create these challenges.

## config_files
All the files used for the setup configuration.

## pages_files
All the pages and files which are needed for the CTF such as: A custom index page.

## challenge_files
All the files which are used in the challenges such as: A description, static files, etc.

## ssl_cert
Add your privatekey and certificate here. Edit nginx.conf if necessary.

## CTFd_setup
<b>No need to modify anything in this one.</b>

Scripts used to create queries and fill the database.   
Also contains the script to check your setup.yml setup.
