from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, LONGTEXT, TEXT, INTEGER, TINYINT, DATETIME, JSON
from sqlalchemy.ext.declarative import declarative_base
from CTFd.utils.crypto import hash_password


Base = declarative_base()

# Challenges
class Challenges(Base):
    __tablename__ = "challenges"
    id = Column('id', INTEGER(11), primary_key=True, nullable=False)
    name = Column('name', VARCHAR(80))
    description = Column('description', TEXT)
    max_attempts = Column('max_attempts', INTEGER(11))
    value = Column('value', INTEGER(11))
    category = Column('category', VARCHAR(80))
    type = Column('type', VARCHAR(80))
    state = Column('state', VARCHAR(80), nullable=False)      
    requirements = Column('requirements', JSON)


def create_challenge(name,description,value,category,type='standard',state='visible',max_attempts=0,requirements=None):
    challenge = Challenges()

    challenge.name = name
    challenge.category = category
    challenge.description = description
    challenge.value = value
    challenge.type = type
    challenge.state = state
    challenge.requirements = requirements
    challenge.max_attempts = max_attempts

    return challenge


# Config
class Config(Base):
    __tablename__ = "config"

    id = Column('id', INTEGER(11), primary_key=True, nullable=False)
    key = Column('key', TEXT)
    value = Column('value', TEXT)


def create_config(key,value):
    config = Config()

    config.key = key
    config.value = value

    return config


# Users
class Users(Base):
    __tablename__ = "users"
    id = Column('id', INTEGER(11), primary_key=True, nullable=False)
    oauth_id = Column('oauth_id',INTEGER(11),unique=True)
    name = Column('name',VARCHAR(128))       
    password = Column('password',VARCHAR(128))   
    email = Column('email',VARCHAR(128),unique=True)      
    type = Column('type',VARCHAR(80))       
    secret = Column('secret',VARCHAR(128))     
    website = Column('website',VARCHAR(128))    
    affiliation = Column('affiliation',VARCHAR(128))
    country = Column('country',VARCHAR(32))    
    bracket = Column('bracket',VARCHAR(32))    
    hidden = Column('hidden',TINYINT(1))     
    banned = Column('banned',TINYINT(1))     
    verified = Column('verified',TINYINT(1))   
    team_id = Column('team_id',INTEGER(11))    
    created = Column('created',DATETIME)    


def create_user(name,password,email,type,hidden=1,banned=0,verified=0,team_id=None,secret=None,website=None,affiliation=None,country=None,bracket=None,oauth_id=None,created=None):
    user = Users()

    user.name = name
    user.password = hash_password(password)
    user.email = email
    user.type = type
    user.website = website
    user.affiliation = affiliation
    user.country = country
    user.hidden = hidden

    return user


# Pages
class Pages(Base):
    __tablename__ = "pages"

    id = Column('id', INTEGER(11), primary_key=True, nullable=False)
    title = Column('title',VARCHAR(80))
    route = Column('route',VARCHAR(80))
    content = Column('content',TEXT)
    draft = Column('draft',TINYINT(1)) 
    hidden = Column('hidden',TINYINT(1)) 
    auth_required = Column('auth_required',TINYINT(1)) 


def create_page(route,content,title=None,draft=0,hidden=None,auth_required=None):
    page = Pages()

    page.title = title
    page.route = route
    page.content = content
    page.draft = draft
    page.hidden = hidden
    page.auth_required = auth_required

    return page


# Files
class Files(Base):
    __tablename__ = "files"

    id = Column('id', INTEGER(11), primary_key=True, nullable=False)
    type = Column('type',VARCHAR(80))
    location = Column('location',TEXT)
    challenge_id = Column('challenge_id',INTEGER(11))
    page_id = Column('page_id',INTEGER(11))

def create_file(type,location,challenge_id=None):
    file = Files()

    file.type = type
    file.location = location
    file.challenge_id = challenge_id

    return file


# Flags
class Flags(Base):
    __tablename__ = "flags"

    id = Column('id', INTEGER(11), primary_key=True, nullable=False)
    challenge_id = Column('challenge_id',INTEGER(11))
    type = Column('type',VARCHAR(80))
    content = Column('content',TEXT)
    data = Column('data',TEXT)

def create_flag(challenge_id,content,type='static',data=None):
    flag = Flags()

    flag.challenge_id = challenge_id
    flag.type = type
    flag.content = content
    flag.data = data

    return flag


# Hints
class Hints(Base):
    __tablename__ = "hints"

    id = Column('id', INTEGER(11), primary_key=True, nullable=False)
    type = Column('type',VARCHAR(80))
    challenge_id = Column('challenge_id',INTEGER(11))
    content = Column('content',TEXT)
    cost = Column('cost',INTEGER(11))
    requirements = Column('requirements',JSON)

def create_hint(challenge_id,content,cost=0,type='standard'):
    hint = Hints()

    hint.challenge_id = challenge_id
    hint.content = content
    hint.cost = cost
    hint.type = type

    return hint


# Tags
class Tags(Base):
    __tablename__ = "tags"

    id = Column('id', INTEGER(11), primary_key=True, nullable=False)
    challenge_id = Column('challenge_id',INTEGER(11))
    value = Column('value',VARCHAR(80))

def create_tag(challenge_id,value):
    tag = Tags()

    tag.challenge_id = challenge_id
    tag.value = value

    return tag
