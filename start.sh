#!/usr/bin/env sh

# Are you using docker-compose challenge containers? Set to 1.
CHALLENGE_COMPOSE=0

# Help
help(){
USAGE="Usage: $0 [OPTION]
Run CTFd with preconfigured setup.yml

Options:
  -s, --start     Start CTFd with preconfigured setup.yml,
                      also starts docker challenges
  -c, --clean     Clean CTFd from any configurations made
  -h, --help      display this help text and exit


Read README.md and docs if in doupt.
Remember to configure setup.yml.
Set 'CHALLENGE_COMPOSE=1' if 'docker-compose up' for challenges is wanted.
" 

printf '%s\n' "$USAGE"
exit 0
}


error(){
printf '%s\n' "$1"
exit 1
}


# Delete 
clean(){
cd CTFd || error 'You need CTFd to use this script'
docker-compose down || error 'You need to pull the submodule down first'
printf 'Cleaning CTFd\n'
[ -d .data ] && rm -rf .data 
git clean -df > /dev/null
git reset --hard > /dev/null
}


# Timezone annoyance, needed for accurate timesetup in CTFd
tz(){
python3 OCD/CTFd_setup/timezone.py > OCD/config_files/tz
}


# Start
start(){
printf 'Checking setup.yml syntax\n'
python3 OCD/CTFd_setup/check_yaml.py OCD/setup.yml || exit 1

printf 'Making sure CTFd is stopped'
cd CTFd && docker-compose down || error 'You need CTFd to use this script'
cd .. || error 'Something went wrong'

printf 'Copying files into CTFd\n'
cp -r --preserve OCD CTFd

# In CTFd directory
cd CTFd || error 'You need CTFd to use this script'

# Setup for entry
tz
mv OCD/CTFd_setup/OCD.py .
mv OCD/CTFd_setup/db.py .

# Needed for YAML in docker
printf 'PyYAML==3.13\n' >> requirements.txt

# Needed for docker CTFd to call OCD.py
INSERTENTRY='# Create the database\necho "Creating database"\npython OCD.py || echo "Skipping database creation"\n\n# Start CTFd'
sed -i "s/^# Start CTFd$/$INSERTENTRY/" docker-entrypoint.sh

# Needed for MariaDB versioning bug
MARIA='    image: mariadb:10.4.12'
sed -i "s/^    image: mariadb:10.4$/$MARIA/" docker-compose.yml


# Start
printf 'Starting CTF\n'
docker-compose up -d > /dev/null

# Wait for website to be running
printf 'Waiting for CTFd to be running\n'
while ! curl -sL localhost:8000 > /dev/null
do
    printf '.'
    sleep 1
done

# Restart cache on setup, skip if already setup
WSITE=$(curl -sL localhost:8000)

case "$WSITE"
in 
    *id=\"setup-form\"*) printf '\nSkipping setup\n' ; 
                         docker-compose rm -sf cache ; 
                         rm -rf .data/redis ;
                         docker-compose up -d cache > /dev/null ;;
    *) printf '\nSetup already done\n' ;;
esac

printf 'CTFd setup done\n'
}


dockerchallenges(){
cd ..

# In CTFdeploy
[ $CHALLENGE_COMPOSE -eq 0 ] && exit 0
[ -f OCD/docker_challenges/docker-compose.yml ] || error 'No docker-compose.yml found in OCD/docker_challenges. Exiting.'
cd OCD/docker_challenges || error 'OCD/docker_challenges is missing' 

printf 'Starting challenge containers\n'
docker-compose up -d

printf 'Docker challenge containers done\n'
}


# cd to start.sh location
cd "$(dirname "$0")" || error 'Something is wrong..'

# Case for intentions
case $1 in
    -s|--start) start; dockerchallenges;;
    -c|--clean) clean ;;
    -h|--help|*) help ;;
esac

exit 0
