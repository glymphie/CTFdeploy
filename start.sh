#!/usr/bin/env sh

# Are you using docker-compose challenge containers? Set to 1.
DOCKER_COMPOSE=0



# Start
cd CTFd

# In CTFd directory
docker-compose up -d > /dev/null

while ! curl -sL localhost:8000 > /dev/null
do
    sleep 1
done

wsite=$(curl -sL localhost:8000)

case "$wsite"
in 
    *id=\"setup-form\"*) echo 'Skipping setup' ; 
                         docker-compose rm -sf cache ; 
                         rm -rf .data/redis ;
                         docker-compose up -d cache > /dev/null ;;
    *) ;;
esac

echo 'Done'
