from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
import pymysql
from db import *

engine = create_engine('mysql+pymysql://root:ctfd@db/ctfd')

# Check if setup already is done
with engine.connect() as con:
    rs = con.execute("SELECT * FROM config WHERE value LIKE '1'")
    for row in rs:
        if row[1] == 'setup' and row[2] == '1':
            con.close()
            quit(1)
con.close()

# Create session
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

CTFList = []



# Create test challenge
CTFList.append(create_challenge('testname',"""test

description""",1337,'testcategory'))


# Create test admin
CTFList.append(create_user('admin','test','coolemail@test.xyz','admin'))

# Create flag
CTFList.append(create_flag(1,'test'))

# Create index page
CTFList.append(create_page('index','<h1>Test Index</h1>'))

# Create config
# name
CTFList.append(create_config('ctf_name','Test CTF name'))
# description
CTFList.append(create_config('ctf_description','Test CTF description'))
# usermode - users or teams
CTFList.append(create_config('user_mode','users'))
# CTF start - epoch 
CTFList.append(create_config('start','1517443260'))
# CTF end - epoch 
CTFList.append(create_config('end','1675209600'))
# CTF freeze scoreboard
CTFList.append(create_config('freeze',None))
# visiblitiy - public or private
CTFList.append(create_config('challenge_visibility','private'))
CTFList.append(create_config('registration_visibility','public'))
CTFList.append(create_config('score_visibility','public'))
CTFList.append(create_config('account_visibility','public'))
# email stuff
CTFList.append(create_config('verify_emails',None))
CTFList.append(create_config('mail_server',None)  )
CTFList.append(create_config('mail_port',None)    )
CTFList.append(create_config('mail_tls',None)     )
CTFList.append(create_config('mail_ssl',None)     )
CTFList.append(create_config('mail_username',None))
CTFList.append(create_config('mail_password',None))
CTFList.append(create_config('mail_useauth',None) )
CTFList.append(create_config('verification_email_subject','Confirm your account for {ctf_name}'))
CTFList.append(create_config('verification_email_body','Please click the following link to confirm your email address for {ctf_name}: {url}'))
CTFList.append(create_config('successful_registration_email_subject','Successfully registered for {ctf_name}'))
CTFList.append(create_config('successful_registration_email_body',"You've successfully registered for {ctf_name}!"))
CTFList.append(create_config('user_creation_email_subject','Message from {ctf_name}'))
CTFList.append(create_config('user_creation_email_body', """An account has been created for you for {ctf_name} at {url}.

Username: {name}
Password: {password}"""))
CTFList.append(create_config('password_reset_subject','Password Reset Request from {ctf_name}'))
CTFList.append(create_config('password_reset_body', """Did you initiate a password reset? If you didn't initiate this request you can ignore this email.

Click the following link to reset your password:
{url}"""))
CTFList.append(create_config('password_change_alert_subject','Password Change Confirmation for {ctf_name}'))
CTFList.append(create_config('password_change_alert_body',"""Your password for {ctf_name} has been changed.

If you didn't request a password change you can reset your password here: {url}"""))
# config setup done
CTFList.append(create_config('setup','1'))
# Extra config
# Whitelist with comma seperated list (test.com, google.com) - or nothing 
CTFList.append(create_config('domain_whitelist',''))
# Team sizes - or NULL
CTFList.append(create_config('team_size',None))
# Allow name change?
CTFList.append(create_config('name_changes','1'))
# Create headers - or NULL
CTFList.append(create_config('theme_header',None))
CTFList.append(create_config('theme_footer',None))
# Create logo - or NULL - f8fdc8de45102187aa65c6173b7d8856/fear.png
CTFList.append(create_config('ctf_logo',None))
# Is the CTF paused?
CTFList.append(create_config('paused','0'))
# Change theme header color
CTFList.append(create_config('theme_header',"""<style id="theme-color">
:root {--theme-color: #000000;}
        .navbar{background-color: var(--theme-color) !important;}
        .jumbotron{background-color: var(--theme-color) !important;}
        </style>"""))


session.add_all(CTFList)
session.commit()

session.close()



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
