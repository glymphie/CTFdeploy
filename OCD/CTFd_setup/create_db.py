import os, posixpath, time, calendar

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
import pymysql, yaml
from werkzeug.utils import secure_filename

from CTFd.utils.encoding import hexencode
from db import *


# Check if setup already is done - close if it is
def check_setup():
    with engine.connect() as con:
        rs = con.execute("SELECT * FROM config WHERE value LIKE '1'")
        for row in rs:
            if row[1] == 'setup' and row[2] == '1':
                con.close()
                quit(1)
    con.close()


# Commit changes of a list of changes
def commit_changes(commitList):
    session.add_all(commitList)
    session.commit()

# Upload file
def upload_file(uploadFile):
# File upload:
# filename = secure_filename(filename)
# md5hash = hexencode(os.urandom(16))
# file_path = posixpath.join(md5hash, filename)


# Go through config and commit
def config_setup(configDict):
    commitList = []
    styleHeader = ''
    configSwitch = {
            'name' : 'ctf_name',
            'description' : 'ctf_description',
            'user_mode' : 'user_mode',
            'team_size' : 'team_size',
            'name_changes' : 'name_changes',
            'theme_footer' : 'theme_footer',
            }

    # Append to commit list
    def commit_to_list(key,value):
            commitList.append(create_config(key,value))

    # Converts time to epoch
    def time_to_epoch(key):
        return calendar.timegm(time.strptime(configDict[key],'%d/%m/%Y %H:%M'))

    # config which is always the same and not currently alterable
    def static_config():
        # CTF freeze scoreboard
        commit_to_list('freeze',None)
        # visiblitiy - public or private
        commit_to_list('challenge_visibility','private')
        commit_to_list('registration_visibility','public')
        commit_to_list('score_visibility','public')
        commit_to_list('account_visibility','public')
        # email stuff
        commit_to_list('verify_emails',None)
        commit_to_list('mail_server',None)
        commit_to_list('mail_port',None)
        commit_to_list('mail_tls',None)
        commit_to_list('mail_ssl',None)
        commit_to_list('mail_username',None)
        commit_to_list('mail_password',None)
        commit_to_list('mail_useauth',None)
        commit_to_list('verification_email_subject','Confirm your account for {ctf_name}')
        commit_to_list('verification_email_body','Please click the following link to confirm your email address for {ctf_name}: {url}')
        commit_to_list('successful_registration_email_subject','Successfully registered for {ctf_name}')
        commit_to_list('successful_registration_email_body',"You've successfully registered for {ctf_name}!")
        commit_to_list('user_creation_email_subject','Message from {ctf_name}')
        commit_to_list('user_creation_email_body', """An account has been created for you for {ctf_name} at {url}.

        Username: {name}
        Password: {password}""")
        commit_to_list('password_reset_subject','Password Reset Request from {ctf_name}')
        commit_to_list('password_reset_body', """Did you initiate a password reset? If you didn't initiate this request you can ignore this email.

        Click the following link to reset your password:
        {url}""")
        commit_to_list('password_change_alert_subject','Password Change Confirmation for {ctf_name}')
        commit_to_list('password_change_alert_body',"""Your password for {ctf_name} has been changed.

        If you didn't request a password change you can reset your password here: {url}""")
        commit_to_list('setup','1')

    static_config()

    for key in configDict.keys():
        # Regular cases for key and value
        try:
            commit_to_list(configSwitch[key],configDict[key])
            continue
        except:
            pass
        
        # Special cases for key and value
        if key == 'start' or key == 'end':
            commit_to_list(key,time.strptime(configDict[key],'%d/%m/%Y %H:%M'))

        elif key == 'whitelist':
            whitelist = ''
            for domain in configDict[key]:
                whitelist += domain + ','
            commit_to_list('domain_whitelist',whitelist[:-1])

        elif key == 'logo':

        elif key == 'theme_header' or key == 'style':
            styleHeader += configDict[key]

        else:
            continue

    if styleHeader != '':
        commit_to_list('theme_header',styleHeader)

    commit_changes(commitList)


# Static config which is always the same:

# Go through users and commit
#def users_setup():

# Go through pages and commit
#def pages_setup():

# Go through pages and commit
#def pages_setup():

# Read the setup.yml file
def read_setup_yaml(YAMLfile)
    with open(YAMLfile,'r') as setup:
        return yaml.safe_load(setup)['CTFd']


def main():
    # Create connection
    engine = create_engine('mysql+pymysql://root:ctfd@db/ctfd')
    # Check if setup is needed
    check_setup()

    # Create session
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Read YAML
    setupYAML = read_setup_yaml('setup.yml')

    # Config setup
    config_setup(setupYAML['config'])

    # Users setup
    #users_setup(setupYAML['users'])

    # Pages setup
    #pages_setup(setupYAML['pages'])

    # Challenges setup
    #challenges_setup(setupYAML['challenges'])

    # Close session
    session.close()


if __name__ == '__main__':
    main()

quit(0)


# Create test challenge
create_challenge('testname',desc,1337,'testcategory')


# Create test admin
create_user('admin','test','coolemail@test.xyz','admin')

# Create flag
create_flag(1,'test')

# Create index page
create_page('index','<h1>Test Index</h1>')

# Create config
# CTF start - epoch 
create_config('start','1517443260')
# CTF end - epoch 
create_config('end','1675209600')
# Extra config
# Whitelist with comma seperated list (test.com, google.com) - or nothing 
create_config('domain_whitelist','')
# Create logo - or NULL - f8fdc8de45102187aa65c6173b7d8856/fear.png
create_config('ctf_logo',None)



# challenges:
# {"prerequisites": [1, 3]}
#
# Flags:
# +----+--------------+--------+---------+------------------+
# | id | challenge_id | type   | content | data             |
# +----+--------------+--------+---------+------------------+
# |  1 |            1 | static | aasdf   |                  |
# |  2 |            1 | regex  | asdffa  | case_insensitive |
# |  3 |            1 | static | sdfsdf  |                  |
# +----+--------------+--------+---------+------------------+
# 
# Hints:
# +----+----------+--------------+---------+------+--------------+
# | id | type     | challenge_id | content | cost | requirements |
# +----+----------+--------------+---------+------+--------------+
# |  1 | standard |            3 | asdf    |   12 | NULL         |
# +----+----------+--------------+---------+------+--------------+
# 
# Tags:
# +----+--------------+---------+
# | id | challenge_id | value   |
# +----+--------------+---------+
# |  1 |            1 | cooltag |
# |  2 |            1 | nice    |
# |  3 |            1 | okay    |
# |  4 |            2 | okay    |
# +----+--------------+---------+
# 
# Files: Hashes?
# +----+-----------+--------------------------------------------------+--------------+---------+
# | id | type      | location                                         | challenge_id | page_id |
# +----+-----------+--------------------------------------------------+--------------+---------+
# |  1 | standard  | f8fdc8de45102187aa65c6173b7d8856/fear.png        |         NULL |    NULL |
# |  2 | page      | 7aed34839b8b77183de7a14817c22a7f/deploy.jpeg     |         NULL |    NULL |
# |  3 | challenge | c34639ca6d2f626e3e99d0656b3fd40a/fear.png        |            2 |    NULL |
# |  4 | challenge | c1e7ecc4d95ae5380b83e5df0da29c79/abomination.png |            3 |    NULL |
# |  5 | challenge | cc823a4880b5b6986e090478890b6a5f/fear.png        |            4 |    NULL |
# +----+-----------+--------------------------------------------------+--------------+---------+
