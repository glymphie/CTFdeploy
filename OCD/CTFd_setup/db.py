"""
Module for creating MySQL queries for CTFd
"""
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, INTEGER, TINYINT, DATETIME, JSON
from sqlalchemy.ext.declarative import declarative_base
from CTFd.utils.crypto import hash_password


Base = declarative_base()

class Config(Base):
    """
    Config
    """
    __tablename__ = "config"

    ID = Column('id', INTEGER(11), primary_key=True, nullable=False)
    key = Column('key', TEXT)
    value = Column('value', TEXT)

    def __init__(self, key, value):
        self.key = key
        self.value = value


class Users(Base):
    """
    Users
    """
    __tablename__ = "users"
    ID = Column('id', INTEGER(11), primary_key=True, nullable=False)
    oauth_id = Column('oauth_id', INTEGER(11), unique=True)
    name = Column('name', VARCHAR(128))
    password = Column('password', VARCHAR(128))
    email = Column('email', VARCHAR(128), unique=True)
    TYPE = Column('type', VARCHAR(80))
    secret = Column('secret', VARCHAR(128))
    website = Column('website', VARCHAR(128))
    affiliation = Column('affiliation', VARCHAR(128))
    country = Column('country', VARCHAR(32))
    bracket = Column('bracket', VARCHAR(32))
    hidden = Column('hidden', TINYINT(1))
    banned = Column('banned', TINYINT(1))
    verified = Column('verified', TINYINT(1))
    team_id = Column('team_id', INTEGER(11))
    created = Column('created', DATETIME)

    def __init__(self, name, **kwargs):
        self.name = name
        self.password = hash_password(kwargs['password'])
        self.email = kwargs['email']
        self.TYPE = kwargs['type']

        self.website = None
        self.affiliation = None
        self.country = None
        self.hidden = 1
        self.verified = 0
        self.banned = 0

        if 'website' in kwargs:
            self.website = kwargs['website']
        if 'affiliation' in kwargs:
            self.affiliation = kwargs['affiliation']
        if 'country' in kwargs:
            self.country = kwargs['country']
        if 'hidden' in kwargs:
            self.hidden = kwargs['hidden']
        if 'verified' in kwargs:
            self.verified = kwargs['verified']
        if 'banned' in kwargs:
            self.banned = kwargs['banned']


class Pages(Base):
    """
    Pages
    """
    __tablename__ = "pages"

    ID = Column('id', INTEGER(11), primary_key=True, nullable=False)
    title = Column('title', VARCHAR(80))
    route = Column('route', VARCHAR(80))
    content = Column('content', TEXT)
    draft = Column('draft', TINYINT(1))
    hidden = Column('hidden', TINYINT(1))
    auth_required = Column('auth_required', TINYINT(1))

    def __init__(self, route, content, **kwargs):
        self.route = route
        self.content = content

        self.title = None
        self.auth_required = None

        if 'title' in kwargs:
            self.title = kwargs['title']
        if 'auth_required' in kwargs:
            self.auth_required = kwargs['auth_required']

        self.draft = 0
        self.hidden = 0


class Files(Base):
    """
    Files
    """
    __tablename__ = "files"

    ID = Column('id', INTEGER(11), primary_key=True, nullable=False)
    TYPE = Column('type', VARCHAR(80))
    location = Column('location', TEXT)
    challenge_id = Column('challenge_id', INTEGER(11))
    page_id = Column('page_id', INTEGER(11))

    def __init__(self, TYPE, location, challenge_id=None):
        self.TYPE = TYPE
        self.location = location
        self.challenge_id = challenge_id



class Challenges(Base):
    """
    Challenges
    """
    __tablename__ = "challenges"
    ID = Column('id', INTEGER(11), primary_key=True, nullable=False)
    name = Column('name', VARCHAR(80))
    description = Column('description', TEXT)
    max_attempts = Column('max_attempts', INTEGER(11))
    value = Column('value', INTEGER(11))
    category = Column('category', VARCHAR(80))
    TYPE = Column('type', VARCHAR(80))
    state = Column('state', VARCHAR(80), nullable=False)
    requirements = Column('requirements', JSON)

    def __init__(self, name, category, description, value, **kwargs):
        self.name = name
        self.category = category
        self.description = description
        self.value = value

        self.max_attempts = 0
        self.requirements = None

        if 'requirements' in kwargs:
            self.requirements = kwargs['requirements']
        if 'max_attempts' in kwargs:
            self.max_attempts = kwargs['max_attempts']

        self.state = 'visible'
        self.TYPE = 'standard'


class Flags(Base):
    """
    Flags
    """
    __tablename__ = "flags"

    ID = Column('id', INTEGER(11), primary_key=True, nullable=False)
    challenge_id = Column('challenge_id', INTEGER(11))
    TYPE = Column('type', VARCHAR(80))
    content = Column('content', TEXT)
    data = Column('data', TEXT)

    def __init__(self, challenge_id, content, **kwargs):
        self.challenge_id = challenge_id
        self.content = content

        self.TYPE = 'static'
        self.data = None

        if 'type' in kwargs:
            self.TYPE = kwargs['type']
        if 'case' in kwargs:
            self.data = kwargs['case']


class Hints(Base):
    """
    Hints
    """
    __tablename__ = "hints"

    ID = Column('id', INTEGER(11), primary_key=True, nullable=False)
    TYPE = Column('type', VARCHAR(80))
    challenge_id = Column('challenge_id', INTEGER(11))
    content = Column('content', TEXT)
    cost = Column('cost', INTEGER(11))
    requirements = Column('requirements', JSON)

    def __init__(self, challenge_id, content, **kwargs):
        self.challenge_id = challenge_id
        self.content = content
        self.cost = 0
        self.TYPE = 'standard'

        if 'cost' in kwargs:
            self.cost = kwargs['cost']
        if 'type' in kwargs:
            self.TYPE = kwargs['type']


class Tags(Base):
    """
    Tags
    """
    __tablename__ = "tags"

    ID = Column('id', INTEGER(11), primary_key=True, nullable=False)
    challenge_id = Column('challenge_id', INTEGER(11))
    value = Column('value', VARCHAR(80))

    def __init__(self, challenge_id, value):
        self.challenge_id = challenge_id
        self.value = value
