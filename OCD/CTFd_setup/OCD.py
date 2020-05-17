import os, sys, posixpath, time, calendar, shutil

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
import pymysql, yaml
from werkzeug.utils import secure_filename

from CTFd.utils.encoding import hexencode
from db import *


# Check if setup already is done - close if it is
def check_setup(engine):
    with engine.connect() as con:
        rs = con.execute("SELECT * FROM config WHERE value LIKE '1'")
        for row in rs:
            if row[1] == 'setup' and row[2] == '1':
                con.close()
                quit(1)
    con.close()


# Commit changes of a list of changes
def commit_changes(session,commitList):
    session.add_all(commitList)
    session.commit()


# Upload file
def upload_file(commitList,type,filename):
    secFilename = secure_filename(filename)
    fileFolder = hexencode(os.urandom(16))
    folderPath = posixpath.join('/','var','uploads',fileFolder)
    filePath = posixpath.join(folderPath,secFilename)
    fileLocation = posixpath.join(fileFolder,secFilename)

    # Make folder to contain file
    os.makedirs(folderPath)
    # Copy file into folder
    shutil.copyfile('OCD/files/' + filename,filePath)

    # Add file to queries
    commitList.append(create_file(type,fileLocation))

    # Return path to file
    return fileLocation

# Go through config and commit
def config_setup(session,setupConfig):
    commitList = []
    styleHeader = ''
    configSwitch = {
        'name' : 'ctf_name',
        'description' : 'ctf_description',
        'user_mode' : 'user_mode',
        'team_size' : 'team_size',
        'name_changes' : 'name_changes',
        'theme_footer' : 'theme_footer'
        }

    # Append to commit list
    def commit_to_list(key,value):
        commitList.append(create_config(key,value))

    # Converts time to epoch
    def time_to_epoch(timekey):
        epoch_time_tz = calendar.timegm(time.strptime(timekey,'%d/%m/%Y %H:%M'))
        return epoch_time_tz

    # config which is always the same and not currently alterable
    def static_config():
        commit_to_list('freeze',None)  # CTF freeze scoreboard
        commit_to_list('challenge_visibility','private') # visiblitiy - public or private v
        commit_to_list('registration_visibility','public')
        commit_to_list('score_visibility','public')
        commit_to_list('account_visibility','public') # email stuff v
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

    for key in setupConfig.keys():
        try: # Regular cases for key and value
            commit_to_list(configSwitch[key],setupConfig[key])
            continue
        except:
            pass
        
        # Special cases for key and value
        if key == 'start' or key == 'end':
            commit_to_list(key,time_to_epoch(setupConfig[key]))

        elif key == 'whitelist':
            whitelist = ''
            for domain in setupConfig[key]:
                whitelist += domain + ','
            commit_to_list('domain_whitelist',whitelist[:-1])

        elif key == 'logo':
            commit_to_list('ctf_logo',upload_file(commitList,'standard',setupConfig[key]))

        elif key == 'theme_header' or key == 'style':
            styleHeader += setupConfig[key]

        else:
            continue

    if styleHeader != '':
        commit_to_list('theme_header',styleHeader)

    commit_changes(session,commitList)


# Go through users and commit
def users_setup(session,setupUsers):
    commitList = []

    for user in setupUsers.keys():
        commitList.append(create_user(user,**setupUsers[user]))

    commit_changes(session,commitList)


# Go through pages and commit
#def pages_setup():

# Go through pages and commit
#def pages_setup():

# Read the setup.yml file
def read_setup_yaml(YAMLfile):
    with open(YAMLfile,'r') as setup:
        return yaml.safe_load(setup)['CTFd']


def main():
    # Create connection
    engine = create_engine('mysql+pymysql://root:ctfd@db/ctfd')
    # Check if setup is needed
    check_setup(engine)

    # Create session
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Read YAML
    setupYAML = read_setup_yaml('OCD/setup.yml')

    # Config setup
    config_setup(session,setupYAML['config'])

    # Users setup
    users_setup(session,setupYAML['users'])

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

# Create flag
create_flag(1,'test')

# Create index page
create_page('index','<h1>Test Index</h1>')



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
