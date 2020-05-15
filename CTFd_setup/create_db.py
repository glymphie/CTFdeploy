from sqlalchemy import Column, ForeignKey, create_engine, inspect
from sqlalchemy.dialects.mysql import VARCHAR, LONGTEXT, TEXT, INTEGER, TINYINT, DATETIME, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pymysql
from CTFd.utils.crypto import hash_password


Base = declarative_base()

class Challenges(Base):
    def __init__(self):
        self.__tablename__ = "challenges"

        self.id = Column('id', INTEGER(11), primary_key=True, nullable=False)
        self.name = Column('name', VARCHAR(80))
        self.description = Column('description', TEXT)
        self.max_attempts = Column('max_attempts', INTEGER(11))
        self.value = Column('value', INTEGER(11))
        self.category = Column('category', VARCHAR(80))
        self.type = Column('type', VARCHAR(80))
        self.state = Column('state', VARCHAR(80), nullable=False)      
        self.requirements = Column('requirements', JSON)

    def create_challenge(self,name,description,value,category,type='standard',state='visible',max_attempts=0,requirements=None):
        self.name = name
        self.category = category
        self.description = description
        self.value = value
        self.type = type
        self.state = state
        self.requirements = requirements
        self.max_attempts = max_attempts


class Config(Base):
    def __init__(self):
        self.__tablename__ = "config"

        self.id = Column('id', INTEGER(11), primary_key=True, nullable=False)
        self.key = Column('key', TEXT)
        self.value = Column('value', TEXT)

    def create_config(self,key,value):
        self.key = key
        self.value = value


class Users(Base):
    def __init__(self):
        self.__tablename__ = "users"

        self.id = Column('id', INTEGER(11), primary_key=True, nullable=False)
        self.oauth_id = Column('oauth_id',INTEGER(11),unique=True)
        self.name = Column('name',VARCHAR(128))       
        self.password = Column('password',VARCHAR(128))   
        self.email = Column('email',VARCHAR(128),unique=True)      
        self.type = Column('type',VARCHAR(80))       
        self.secret = Column('secret',VARCHAR(128))     
        self.website = Column('website',VARCHAR(128))    
        self.affiliation = Column('affiliation',VARCHAR(128))
        self.country = Column('country',VARCHAR(32))    
        self.bracket = Column('bracket',VARCHAR(32))    
        self.hidden = Column('hidden',TINYINT(1))     
        self.banned = Column('banned',TINYINT(1))     
        self.verified = Column('verified',TINYINT(1))   
        self.team_id = Column('team_id',INTEGER(11))    
        self.created = Column('created',DATETIME)    

    def create_user(self,name,password,email,type,hidden=1,banned=0,verified=0,team_id=None,secret=None,website=None,affiliation=None,country=None,bracket=None,oauth_id=None,created=None):
        self.name = name
        self.password = hash_password(password)
        self.email = email
        self.type = type
        self.website = website
        self.affiliation = affiliation
        self.country = country
        self.hidden = hidden


class Pages(Base):
    def __init__(self):
        self.__tablename__ = "pages"

        self.id = Column('id', INTEGER(11), primary_key=True, nullable=False)
        self.title = Column('title',VARCHAR(80))
        self.route = Column('route',VARCHAR(80))
        self.content = Column('content',TEXT)
        self.draft = Column('draft',TINYINT(1)) 
        self.hidden = Column('hidden',TINYINT(1)) 
        self.auth_required = Column('auth_required',TINYINT(1)) 

    def create_page(self,route,content,title=None,draft=0,hidden=None,auth_required=None):
        self.title = title
        self.route = route
        self.content = content
        self.draft = draft
        self.hidden = hidden
        self.auth_required = auth_required


class Files(Base):
    def __init__(self):
        self.__tablename__ = "files"

        self.id = Column('id', INTEGER(11), primary_key=True, nullable=False)
        self.type = Column('type',VARCHAR(80))
        self.location = Column('location',TEXT)
        self.challenge_id = Column('challenge_id',INTEGER(11))
        self.page_id = Column('page_id',INTEGER(11))

    def create_file(self,type,location,challenge_id=None):
        self.type = type
        self.location = location
        self.challenge_id = challenge_id


class Flags(Base):
    def __init__(self):
        self.__tablename__ = "flags"

        self.id = Column('id', INTEGER(11), primary_key=True, nullable=False)
        self.challenge_id = Column('challenge_id',INTEGER(11))
        self.type = Column('type',VARCHAR(80))
        self.content = Column('content',TEXT)
        self.data = Column('data',TEXT)

    def create_flag(self,challenge_id,content,type='static',data=None):
        self.challenge_id = challenge_id
        self.type = type
        self.content = content
        self.data = data


class Hints(Base):
    def __init__(self):
        self.__tablename__ = "hints"

        self.id = Column('id', INTEGER(11), primary_key=True, nullable=False)
        self.type = Column('type',VARCHAR(80))
        self.challenge_id = Column('challenge_id',INTEGER(11))
        self.content = Column('content',TEXT)
        self.cost = Column('cost',INTEGER(11))
        self.requirements = Column('requirements',JSON)

    def create_hint(self,challenge_id,content,cost=0,type='standard'):
        self.challenge_id = challenge_id
        self.content = content
        self.cost = cost
        self.type = type


class Tags(Base):
    def __init__(self):
        self.__tablename__ = "tags"

        self.id = Column('id', INTEGER(11), primary_key=True, nullable=False)
        self.challenge_id = Column('challenge_id',INTEGER(11))
        self.value = Column('value',VARCHAR(80))

    def create_tag(self,challenge_id,value):
        self.challenge_id = challenge_id
        self.value = value


engine = create_engine('mysql+pymysql://root:ctfd@db/ctfd')

with engine.connect() as con:
    rs = con.execute("SELECT * FROM config WHERE value LIKE '1'")
    for row in rs:
        if row[1] == 'setup' and row[2] == '1':
            con.close()
            quit(1)
con.close()


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

CTFList = []



# Create test challenge
create_challenge('testname','testdescription',1337,'testcategory')

# Create test admin
create_user('test admin','test','coolemail@test.xyz','admin')

# Create index page
create_page('index','<h1>Test Index</h1>')

# Create config
# name
create_config('ctf_name','Test CTF name')
# description
create_config('ctf_description','Test CTF description')
# usermode - users or teams
create_config('user_mode','users')
# CTF start - epoch 
create_config('start','1517443260')
# CTF end - epoch 
create_config('end','1675209600')
# CTF freeze scoreboard
create_config('freeze',None)
# visiblitiy - public or private
create_config('challenge_visibility','private')
create_config('registration_visibility','public')
create_config('score_visibility','public')
create_config('account_visibility','public')
# email stuff
create_config('verify_emails',None)
create_config('mail_server',None)  
create_config('mail_port',None)    
create_config('mail_tls',None)     
create_config('mail_ssl',None)     
create_config('mail_username',None)
create_config('mail_password',None)
create_config('mail_useauth',None) 
create_config('verification_email_subject','Confirm your account for {ctf_name}')
create_config('verification_email_body','Please click the following link to confirm your email address for {ctf_name}: {url}')
create_config('successful_registration_email_subject','Successfully registered for {ctf_name}')
create_config('successful_registration_email_body',"You've successfully registered for {ctf_name}!")
create_config('user_creation_email_subject','Message from {ctf_name}')
create_config('user_creation_email_body', """An account has been created for you for {ctf_name} at {url}.

Username: {name}
Password: {password}""")
create_config('password_reset_subject','Password Reset Request from {ctf_name}')
create_config('password_reset_body', """Did you initiate a password reset? If you didn't initiate this request you can ignore this email.

Click the following link to reset your password:
{url}""")
create_config('password_change_alert_subject','Password Change Confirmation for {ctf_name}')
create_config('password_change_alert_body',"""Your password for {ctf_name} has been changed.

If you didn't request a password change you can reset your password here: {url}""")
# config setup done
create_config('setup','1')
# Extra config
# Whitelist with comma seperated list (test.com, google.com) - or nothing 
create_config('domain_whitelist','')
# Team sizes - or NULL
create_config('team_size','NULL')
# Allow name change?
create_config('name_changes','1')
# Create headers - or NULL
create_config('theme_header','NULL')
create_config('theme_footer','NULL')
# Create logo - or NULL - f8fdc8de45102187aa65c6173b7d8856/fear.png
create_config('ctf_logo','NULL')
# Is the CTF paused?
create_config('paused','0')
# Change theme header color
create_config('theme_header',"""<style id="theme-color">
:root {--theme-color: #000000;}
        .navbar{background-color: var(--theme-color) !important;}
        .jumbotron{background-color: var(--theme-color) !important;}
        </style>""")

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
# +----+--------------+-------+
# | id | challenge_id | value |
# +----+--------------+-------+
# |  1 |            3 | fdsf  |
# |  2 |            1 | fdsf  |
# +----+--------------+-------+
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
