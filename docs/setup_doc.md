# Documentation for CTFdeploy
An overview of what is happening and why some decisions were made in the creation of these scripts.

## start.sh
The orchestration of the whole setup is controlled by this simple script. The first thing the script does is check what flag is set and execute accordingly.   
<b>`start.sh` needs sudo/root to remove some root owned files, .data/redis in CTFd. This is to speed up the deployment.</b>

### ./start.sh -s
When the script starts with the -s flag:  
  1. Is runs `check_yaml.py` against `setup.yml`. This should capture any mistakes which were made when creating the `setup.yml` file. If `setup.yml` seems fine it will continue. Or else an error will be displayed with a message on what seems wrong with `setup.yml`.
  2. Copy all the files into `CTFd`. Another step here is to check what timezone the computer is set to. This is to account for time difference artifacts in CTFd and make sure the time set is to the correct timezone. It essentially just looks in `/etc/localtime` and parses it to `OCD.py` which will do calculations according to the timezone.
  3. Requirements are pushed to `CTFd`:   
    - PyYAML is required on the `CTFd` docker container.   
    - The `CTFd` `docker-entrypoint.sh` needs to call `OCD.py` when it starts up, so this is pushed to `docker-entrypoint.sh`.  
    - Last is a current issue with `CTFd` and `MariaDB`, a wrong version is pulled from docker-hub, this is corrected.  
  4. Docker-compose starts the `CTFd` server.
  5. It waits for the `CTFd` website to be reachable, and checks if `setup-form` is present, which means it's trying to do a new `CTFd` setup instance. This can be skipped so if it's present the `redis` cache server is cleared and restarted so the preconfigured setup can be used almost instantly. Alternatively, the `redis` server needs 5 minutes to clear its cache, however, restarting is faster.
  6. CTFd is up and running.
  7. If `CHALLENGE_COMPOSE` is set to `1`, it will try to start up the containers stored in `OCD/docker_challenges`. This is just for convenience and can be skipped if you prefer to start the containers separately.

### ./start.sh -c
<b>Make sure to stop CTFd, MariaDB, and redis container before cleaning.</b>

When the script starts with the -c flag:  
  1. Remove `.data` in `CTFd` - this is where all data is stored from the containers.
  2. Clean all files not tracked in `CTFd`.

## OCD.py
The database creation is handled by `OCD.py` while in the `CTFd` docker container. It goes through the `setup.yml` file and creates queries according to what is wanted in the setup of CTFd. The reason for `check_yaml.py` is due to the fact some queries must be present for CTFd to work properly. It will still check if the `optional` setup configurations are set and make queries accordingly. `OCD.py` uses [sqlalchemy](https://www.sqlalchemy.org/) to construct queries just as `CTFd` would do while it's running. 

Even after setup, CTFd can be configured. This configuration is however not associated with CTFdeploy but can be extracted and imported with CTFd's import/export feature. 
