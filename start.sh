#!/usr/bin/env sh


# Are you using docker-compose challenge containers? Set to 1.
CHALLENGE_COMPOSE=0


# Are you using an SSL Certificate? Set to 1.
NGINX_SSL=0
# Set hostname to your URL.
hostname='host'
# Set cert to your certificate filename.
cert='cert'
# Set key to your private key filename.
key='key'



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

printf '%s' "$USAGE"
exit 0
}


error(){
printf '%s\nExiting.\n' "$1"
exit 1
}


# Delete 
clean(){
cd CTFd || error 'You need CTFd to use this script'
docker-compose down || error 'You need to pull the submodule down first'
printf 'Cleaning CTFd\n'
[ -d .data ] && rm -rf .data 
git checkout -- . > /dev/null
git clean -df . > /dev/null
}


# Timezone annoyance, needed for accurate timesetup in CTFd
tz(){
python3 OCD/CTFd_setup/timezone.py > OCD/config_files/tz
}


# Setup for nginx HTTPS
nginxssl(){
if [ -f OCD/ssl_cert/"$cert" ]; then
    grep -q 'CERTIFICATE' OCD/ssl_cert/"$cert" || error 'Missing Certificate.' 
    cp OCD/ssl_cert/"$cert" CTFd/conf/nginx/. 
else
    error 'Missing Certificate.'
fi

if [ -f OCD/ssl_cert/"$key" ]; then
    grep -q 'PRIVATE KEY' OCD/ssl_cert/"$key" || error 'Missing Private Key.' 
    cp OCD/ssl_cert/"$key" CTFd/conf/nginx/. 
else
    error 'Missing Private Key.' 
fi

printf 'Setting up SSL\n'

sed -i 's/^      - \.\/conf\/nginx\/http\.conf:\/etc\/nginx\/nginx\.conf$/      - \.\/conf\/nginx:\/etc\/nginx/' CTFd/docker-compose.yml
sed -i 's/^      - 80:80$/      - 80:80\n      - 443:443/' CTFd/docker-compose.yml

rm CTFd/conf/nginx/http.conf 2> /dev/null
python3 OCD/CTFd_setup/setup_nginx.py "$hostname" "$cert" "$key"
}


# Start
start(){
printf 'Checking setup.yml syntax\n'
python3 OCD/CTFd_setup/check_yaml.py OCD/setup.yml || exit 1

printf 'Making sure CTFd is stopped\n'
cd CTFd || error 'You need CTFd to use this script'
docker-compose down || error 'You need to pull the submodule down first'
cd .. || error 'Something went wrong'

printf 'Copying files into CTFd\n'
cp -r --preserve OCD CTFd

# Check for SSL setup
[ $NGINX_SSL -eq 1 ] && nginxssl

# In CTFd directory
cd CTFd || error 'You need CTFd to use this script'

# Setup for entry
tz
mv OCD/CTFd_setup/OCD.py .
mv OCD/CTFd_setup/db.py .

# Needed for YAML in docker
grep -q 'PyYAML==3.13' requirements.txt || printf 'PyYAML==3.13\n' >> requirements.txt

# Needed for docker CTFd to call OCD.py
grep -q "# Create the database" docker-entrypoint.sh || sed -i "s/^# Start CTFd$/$INSERTENTRY/" docker-entrypoint.sh

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

[ $CHALLENGE_COMPOSE -eq 1 ] && dockerchallenges
}


dockerchallenges(){
cd ..

# In CTFdeploy
[ -f OCD/docker_challenges/docker-compose.yml ] || error 'No docker-compose.yml found in OCD/docker_challenges.'
cd OCD/docker_challenges || error 'OCD/docker_challenges is missing' 

printf 'Starting challenge containers\n'
docker-compose up -d

printf 'Docker challenge containers done\n'
}


# cd to start.sh location
cd "$(dirname "$0")" || error 'Something is wrong..'

INSERTENTRY='# Create the database\necho \"Creating database\"\npython OCD.py || echo \"Skipping database creation\"\n# Start CTFd'

# Case for intentions
case $1 in
    -s|--start) start ;;
    -c|--clean) clean ;;
    -h|--help|*) help ;;
esac

exit 0
