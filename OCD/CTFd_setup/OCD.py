import os, posixpath, time, calendar, shutil, re

from sqlalchemy import create_engine, update, select
from sqlalchemy.orm import sessionmaker
import pymysql, yaml
from werkzeug.utils import secure_filename

from CTFd.utils.encoding import hexencode
from db import *


# Check if setup already is done - close if it is
def check_setup(engine):
    with engine.connect() as conn:
        for row in conn.execute(select([Config]).where(Config.key == 'setup')):
            if row[2] == '1':
                quit(1)
    conn.close()

# Commit changes of a list of changes
def commit_changes(session,commitList):
    session.add_all(commitList)
    session.commit()


# Upload file
def upload_file(commitList,type,filename,challenge_id=None):
    secFilename = secure_filename(filename[filename.rfind('/') + 1:])
    fileFolder = hexencode(os.urandom(16))
    folderPath = posixpath.join('/','var','uploads',fileFolder)
    filePath = posixpath.join(folderPath,secFilename)
    fileLocation = posixpath.join(fileFolder,secFilename)

    # Make folder to contain file
    os.makedirs(folderPath)
    # Copy file into folder
    shutil.copyfile('OCD/' + filename,filePath)

    # Add file to queries
    commitList.append(create_file(type,fileLocation,challenge_id))

    # Return path to file
    return fileLocation

# Go through config and commit
def config_setup(session,setupConfig):
    commitList = []

    # Append to commit list
    def commit_to_list(key,value):
        commitList.append(create_config(key,value))


    # Converts time to epoch
    def time_to_epoch(timekey):
        with open('OCD/config_files/tz','r') as tz:
            timediff = tz.readline()[:-1].split(':')
            if len(timediff) <= 1:
                diff = int(timediff[0]) * 60 * 60
            if len(timediff) == 2:
                if timediff[0][0] == '-':
                    diff -= int(timediff[1]) * 60
                else:
                    diff += int(timediff[1]) * 60
            return (calendar.timegm(time.strptime(timekey,'%d/%m/%Y %H:%M')) + diff)


    # config which is always the same and not currently alterable
    def static_config():
        commit_to_list('ctf_name',setupConfig['name'])
        commit_to_list('ctf_description',setupConfig['description'])
        commit_to_list('user_mode',setupConfig['user_mode'])
        commit_to_list('start',time_to_epoch(setupConfig['start']))
        commit_to_list('end',time_to_epoch(setupConfig['end']))

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


    # Commit config to db
    styleHeader = ''
    static_config()

    # Go through extra settings in config
    if 'whitelist' in setupConfig:
        whitelist = ''
        for domain in setupConfig['whitelist']:
            whitelist += domain + ','
        commit_to_list('domain_whitelist',whitelist[:-1])

    if 'team_size' in setupConfig:
        commit_to_list('team_size',setupConfig['team_size'])

    if 'name_changes' in setupConfig:
        commit_to_list('name_changes',setupConfig['name_changes'])

    if 'logo' in setupConfig:
        commit_to_list('ctf_logo',upload_file(commitList,'standard','config_files/' + setupConfig['logo']))

    if 'style' in setupConfig:
        with open('OCD/config_files/' + setupConfig['style'],'r') as style:
            styleHeader += ''.join(style.readlines())

    if 'theme_header' in setupConfig:
        with open('OCD/config_files/' + setupConfig['theme_header'],'r') as header:
            styleHeader += ''.join(header.readlines())
        commit_to_list('theme_header',styleHeader)

    if 'theme_footer' in setupConfig:
        with open('OCD/config_files/' + setupConfig['theme_footer'],'r') as footer:
            commit_to_list('theme_footer',''.join(footer.readlines()))

    commit_changes(session,commitList)


# Go through users and commit
def users_setup(session,setupUsers):
    commitList = []

    for user in setupUsers:
        commitList.append(create_user(user,**setupUsers[user]))

    commit_changes(session,commitList)


# Go through pages and commit
def pages_setup(session,setupPages):
    commitList = []

    # Create all pages
    for route in setupPages:
        kwargs = dict()

        with open('OCD/pages_files/' + setupPages[route]['page'],'r') as pageFile:
            page = pageFile.read()

        # Go through extra settings
        if 'file' in setupPages[route]:
            for picture in setupPages[route]['file']:
                pictureLocaiton = upload_file(commitList,'page','pages_files/' + picture)
                # Replace the filename with new random folder from upload
                page = page.replace('src="' + picture + '"','src="files/' + pictureLocaiton + '"')
                page = page.replace("src='" + picture + "'","src='files/" + pictureLocaiton + "'")

        if 'title' in setupPages[route]:
            kwargs['title'] = setupPages[route]['title']

        if 'auth_required' in setupPages[route]:
            kwargs['auth_required'] = setupPages[route]['auth_required']

        commitList.append(create_page(route,page,**kwargs))

    commit_changes(session,commitList)


# Go through challenges and commit
def challenges_setup(session,setupChallenges):
    commitList = []

    # Create all challenges
    for category in setupChallenges:
        for challenge in setupChallenges[category]:
            kwargs = dict()
            
            with open('OCD/challenge_files/' + setupChallenges[category][challenge]['description']) as desc:
                description = desc.read()

            if 'max_attempts' in setupChallenges[category][challenge]:
                kwargs['max_attempts'] = setupChallenges[category][challenge]['max_attempts']
            commitList.append(create_challenge(challenge,category,description,setupChallenges[category][challenge]['value'],**kwargs))
            commit_changes(session,commitList)


# Assign flags, tags, hints, files, and requirements to challenges
def extras_for_challenges(engine,session,setupChallenges):
    commitList = []

    # Query for challenge id
    def get_challenge_id(challenge):
        with engine.connect() as conn:
            for row in conn.execute(select([Challenges]).where(Challenges.name == challenge)):
                chall_id = int(row[0])
        conn.close()

        return chall_id

    # Setup flags
    def flags_setup():
        kwargs = dict()
        for config in setupChallenges[category][challenge]['flag']:

            if 'type' in setupChallenges[category][challenge]['flag']:
                kwargs['type'] = setupChallenges[category][challenge]['flag']['type']
            if 'case' in setupChallenges[category][challenge]['flag']: 
                if setupChallenges[category][challenge]['flag']['case'] == 'insensitive':
                    kwargs['case'] = 'case_insensitive'

        commitList.append(create_flag(get_challenge_id(challenge),setupChallenges[category][challenge]['flag']['flag'],**kwargs))


    # Setup tags
    def tags_setup():
        if 'tag' in setupChallenges[category][challenge]:
            chal_id = get_challenge_id(challenge)
            for tag in setupChallenges[category][challenge]['tag']:
                commitList.append(create_tag(chal_id,tag))


    # Setup challenge files
    def file_setup():
        if 'file' in setupChallenges[category][challenge]:
            chal_id = get_challenge_id(challenge)
            for challengeFile in setupChallenges[category][challenge]['file']:
                upload_file(commitList,'challenge','challenge_files/' + challengeFile,challenge_id=chal_id)

    
    # Setup hints
    def hint_setup():
        matches = [hint for hint in setupChallenges[category][challenge] if re.match(re.compile('hint*'),hint)]
        chal_id = get_challenge_id(challenge)

        for hint in matches:
            kwargs = dict()
            if 'cost' in setupChallenges[category][challenge][hint]:
                kwargs['cost'] = setupChallenges[category][challenge][hint]['cost']

            with open('OCD/challenge_files/' + setupChallenges[category][challenge][hint]['description'],'r') as desc:
                description = desc.read()

            commitList.append(create_hint(chal_id,description,**kwargs))


    # Setup requirements
    def requirements_setup():
        if 'requirements' in setupChallenges[category][challenge]:
            requirementsJSON = dict()
            reqIDs = []
            for reqChal in setupChallenges[category][challenge]['requirements']:
                reqIDs.append(get_challenge_id(reqChal))

            requirementsJSON['prerequisites'] = reqIDs

            with engine.connect() as conn:
                conn.execute(update(Challenges).where(Challenges.name==challenge).values(requirements=requirementsJSON))
            conn.close()


    # Update challenges
    for category in setupChallenges:
        for challenge in setupChallenges[category]:
            # Setup flags
            flags_setup()

            # Setup tags
            tags_setup()

            # Setup files
            file_setup()

            # Setup hints
            hint_setup()

            # Setup hints
            requirements_setup()

    commit_changes(session,commitList)

            

# Read the setup.yml file
def read_setup_yaml(YAMLfile):
    with open(YAMLfile,'r') as setup:
        return yaml.safe_load(setup)['CTFd']


def main():
    # Create connection
    engine = create_engine('mysql+pymysql://root:ctfd@db/ctfd')

    # Create session
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if setup is needed
    check_setup(engine)

    # Read YAML
    setupYAML = read_setup_yaml('OCD/setup.yml')

    # Config setup
    config_setup(session,setupYAML['config'])

    # Users setup
    users_setup(session,setupYAML['users'])

    # Pages setup
    pages_setup(session,setupYAML['pages'])

    # Challenges setup
    challenges_setup(session,setupYAML['challenges'])

    # Assign tags, hints, files, and requirements to challenges
    extras_for_challenges(engine,session,setupYAML['challenges'])

    # Close session
    session.close()


if __name__ == '__main__':
    main()

quit(0)
