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

# Introduction
This is how good it is.

# Guide

## Dependencies
Local setup:
  1. Docker, [Install docker](https://docs.docker.com/get-docker/).
  2. Docker-compose, [Install docker-compose](https://docs.docker.com/compose/install/).
  3. CTFd, pull CTFd in CTFdeploy as a submodule: `git submodule update --init --recursive`

Remote setup:
  - WIP

### YAML
The setup is controlled by a YAML file. The different sections control how the 
CTF is setup. 

Make sure `setup.yml` is configured to your liking. It is located in [OCD](OCD/setup.yml).

### [Documentation](docs/yaml_setup.md).

## Start
    1. Configure [setup.yml](OCD/setup.yml).
    2. Move used files into [files](OCD/files).
    3. Move used pages into [pages](OCD/pages).
    4. <b>OPTIONAL</b>: Configure docker containers in [pages](OCD/docker_challenges) and make
       a `docker-compose.yml` file for these containers.
        -  Edit `DOCKER_COMPOSE` in `start.sh` if you want it to start your challenge containers 
           for you via docker-compose. 

Start the CTFd server.

`./start`

# How does it work?

### [Documentation](docs/setup_doc.md).

# References
### [CTFd](https://github.com/CTFd/CTFd)
The project is based upon the CTFd CTF-framework and is a modification-script of 
this software. The project is not using a modified version of CTFd but is a
separate project.

##### [Project Plan](docs/project_plan.md)
The project plan is for school purposes.

`OCD = One-Click Deployment`
