from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, LONGTEXT, TEXT, INTEGER, TINYINT, DATETIME, JSON
from sqlalchemy.ext.declarative import declarative_base
from CTFd.utils.crypto import hash_password


Base = declarative_base()

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


def create_user(name,**kwargs):
    user = Users()

    user.name = name
    user.password = hash_password(kwargs['password'])
    user.email = kwargs['email']
    user.type = kwargs['type']

    user.website = None
    user.affiliation = None
    user.country = None
    user.hidden = 1
    user.verified = 0
    user.banned = 0

    if 'website' in kwargs:
        user.website = kwargs['website']
    if 'affiliation' in kwargs:
        user.affiliation = kwargs['affiliation']
    if 'country' in kwargs:
        user.country = kwargs['country']
    if 'hidden' in kwargs:
        user.hidden = kwargs['hidden']
    if 'verified' in kwargs:
        user.verified = kwargs['verified']
    if 'banned' in kwargs:
        user.banned = kwargs['banned']

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


def create_page(route,content,**kwargs):
    page = Pages()

    page.route = route
    page.content = content

    page.title = None
    page.auth_required = None

    page.draft = 0
    page.hidden = 0

    if 'title' in kwargs:
        page.title = kwargs['title']
    if 'auth_required' in kwargs:
        page.auth_required = kwargs['auth_required']

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


def create_challenge(name,category,description,value,**kwargs):
    challenge = Challenges()

    challenge.name = name
    challenge.category = category
    challenge.description = description
    challenge.value = value

    challenge.max_attempts = 0
    challenge.requirements = None

    if 'requirements' in kwargs:
        challenge.requirements = kwargs['requirements']
    if 'max_attempts' in kwargs:
        challenge.max_attempts = kwargs['max_attempts']

    challenge.state = 'visible'
    challenge.type = 'standard'

    return challenge


# Flags
class Flags(Base):
    __tablename__ = "flags"

    id = Column('id', INTEGER(11), primary_key=True, nullable=False)
    challenge_id = Column('challenge_id',INTEGER(11))
    type = Column('type',VARCHAR(80))
    content = Column('content',TEXT)
    data = Column('data',TEXT)

def create_flag(challenge_id,content,**kwargs):
    flag = Flags()

    flag.challenge_id = challenge_id
    flag.content = content

    flag.type = 'static'
    flag.data = None

    if 'type' in kwargs:
        flag.type = kwargs['type']
    if 'case' in kwargs:
        flag.data = kwargs['case']

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

def create_hint(challenge_id,content,**kwargs):
    hint = Hints()

    hint.challenge_id = challenge_id
    hint.content = content
    hint.cost = 0
    hint.type = 'standard'

    if 'cost' in kwargs:
        hint.cost = kwargs['cost']
    if 'type' in kwargs:
        hint.type = kwargs['type']

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
