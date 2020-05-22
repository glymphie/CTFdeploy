# CTFdeployment
This deployment script is used for <b>FRESH</b> deployments of CTFd in docker. 
Used to cut the time of deployment on new instances of CTFd. Can be customized 
for specific config, admins, challenges, and pages, as to skip the setup step 
for a premade CTF.

Not meant to replace export/import from CTFd, rather used for <b>FRESH</b> deployments.

Make sure to read through the [CTFd](https://github.com/CTFd/CTFd) documentation
and install their dependencies before using this script, as it is dependent on
it.

<b>Only tested on Linux.</b>

# Guide

### Dependencies
##### Local setup:
  1. Docker, [Install docker](https://docs.docker.com/get-docker/).
  2. Docker-compose, [Install docker-compose](https://docs.docker.com/compose/install/).
  3. CTFd, pull CTFd in CTFdeploy as a submodule: `git submodule update --init --recursive`
  4. Python3, PyYAML, pycountry  
    - `python3 -m pip install -r requirements.txt`   
        - `PyYAML`: Used to check for syntax errors in `setup.yml` before deployment.  
        - `pycountry`: Used to check the countrycode given to users when going through `setup.yml` syntax.
  5. Curl, install either via your package manager or from source.

##### Remote setup:
  - WIP

### YAML
The setup is controlled by a single YAML file. The different sections control how the 
CTF is setup. 

Make sure `setup.yml` is configured to your liking. It is located in [OCD/setup.yml](OCD/setup.yml).

### [Documentation](docs/yaml_setup.md).

## Start
  1. Configure [setup.yml](OCD/setup.yml).
  2. Move used files into their folders.   
    - For config - [OCD/config_files](OCD/config_files).  
    - For pages - [OCD/pages_files](OCD/pages_files).  
    - For challenges - [OCD/challenge_files](OCD/challenge_files).  
  4. <b>OPTIONAL</b>: Configure docker containers in [OCD/docker_challenges](OCD/docker_challenges) and make a `docker-compose.yml` file for these containers.   
    - Edit `DOCKER_COMPOSE` in `start.sh` if you want it to start your challenge containers for you via docker-compose. 
  5. Start the CTFd server  
    - sudo `./start -s`  

## Stop and cleaning up
Stopping the containers is done normally via docker-compose while in the CTFd folder.

`docker-compose down`

Clean up CTFd if you changed your mind and want to start over. <b>Doesn't touch your config in CTFdeploy.</b>

`sudo ./start -c`

This resets altered files, removes CTFdeploy files, and clears the cache so CTFd can be started from fresh again.

# How does it work?

### [Documentation](docs/setup_doc.md).

# Notice
<b>CTFdeploy will alter the following files in CTFd: requirements.txt, docker-compose.yml, and docker-entrypoint.sh. This is to integrate CTFdeploy, read through the documentation and read the source code if you are in doubt about either integrity or safety.</b>

# References

### [CTFd](https://github.com/CTFd/CTFd)
The project is based upon the CTFd CTF-framework and is a modification-script of 
this software. The project is not using a forked version of CTFd but is a
separate project related to CTFd and dependent on it.

##### [Project Plan](docs/project_plan.md)
The project plan is for school purposes.

`OCD = One-Click Deployment`
