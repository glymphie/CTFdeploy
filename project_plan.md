# Project Plan

## Background
The idea behind this project is the issue of manual deployment of CTFd. 
Deployment might not be an issue when dealing with a small amount of challenges 
but after some time it gets tedious. 


## Purpose 
The purpose of this project is to leverage the time spent on deploying CTF 
challenges with [CTFd](https://github.com/CTFd/CTFd).

The project is completed with satisfaction when all major goals are met. Extra
goals are convenient but not critical to the success of the project. 


## Goals
The project has a couple of 'Main Goals' which are critical to the success of
the project.

The challenges should be populated in the CTFd database so no manual setup is
required.
- [ ] Population of challenges in CTFd.

Custom index page deployment as with challenges.
- [ ] Show custom index page.

All challenges which need to be hosted in docker containers should be deployed.
- [ ] Deployment of challenges in docker containers.

Testing script setup for 'completed' project.
- [ ] Automated deployment of CTFd.

#### Extra goals
Default is HTTP, HTTPS would be nice.
- [ ] HTTPS nginx frontend.

Error handler for docker containers, notification, log, and restart container.
- [ ] Docker container monitoring.

Limit docker resources to prevent crashing/hang.
- [ ] Docker log, CPU, & MEM resources.

Develop challenge documentation.
- [ ] 'Creating a challenge' documentation.
    - [ ] Hardware challenges.

Docker swarm or kubernetes, for remote deployment.
- [ ] Remote deployment.


## Schedule
The project is scheduled to last from 13:00 01/04-2020 to 13:00 02/06/2020.

Schedule around goals and extra goals can be found under
[milestones](https://gitlab.com/Glymph-PHS/CTFdeploy/-/milestones).


## Organization
Project members:

|**Name**|**Website**|**Email**|
|---|---|---|
| Peter Husted Simonsen | https://glymph.xyz | pete58f8@edu.ucl.dk |

Mentors:

|**Name**|**Email**|
|---|---|
|Nikolaj Peter Esbjørn Simonsen| nisi@ucl.dk|


## Risk assessment

#### Documentation
* Lack of documentation.
    * No documentation on project creates problems on showing what you did.
    * Lack of documentation on topics doesn't show what I've learned.

#### Planning
* No planning.
    * No planning creates problems with deadlines.
    * Issues on handing in on time.

#### Communication
* Unclear objectives.
    * Communication mentor to create an awesome project.


## Stakeholders
##### Project members
If the project members fail at creating/making the project, they will lack
knowledge and might fail education.

##### End users
If the end users doesn't understand how to use the project they will not want to
use it. This will also make them dissatisfied.

##### Mentor
If the mentor isn't satisfied with the project they might fail the student.


## Communication
Communication can be either on [Gitlab in form of
issues](https://gitlab.com/Glymph-PHS/CTFdeploy/-/issues) or [via
email](mailto:pete58f8@edu.ucl.dk).

Mentor will be contacted either via [email](mailto:nisi@ucl.dk), 
[riot](https://riot.im), or in person.


## Perspectives
This project will serve as a final project for the education of IT-technology on
UCL, Odense.

The project is reflecting on a "real" issue created by PwC in their cyber
department as CTF deployment might waste time on a repetitive task.


## Evaluation


## References
### [CTFd](https://github.com/CTFd/CTFd)
