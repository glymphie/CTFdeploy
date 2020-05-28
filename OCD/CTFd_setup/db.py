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

        self.website = kwargs['website'] if 'website' in kwargs else None
        self.affiliation = kwargs['affiliation'] if 'affiliation' in kwargs else None
        self.country = kwargs['country'] if 'country' in kwargs else None
        self.hidden = kwargs['hidden'] if 'hidden' in kwargs else 1
        self.verified = kwargs['verified'] if 'verified' in kwargs else 0
        self.banned = kwargs['banned'] if 'banned' in kwargs else 0


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

        self.draft = 0
        self.hidden = 0

        self.title = kwargs['title'] if 'title' in kwargs else None
        self.auth_required = kwargs['auth_required'] if 'auth_required' in kwargs else None


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

        self.requirements = kwargs['requirements'] if 'requirements' in kwargs else None
        self.max_attempts = kwargs['max_attempts'] if 'max_attempts' in kwargs else 0

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
        self.cost = 0
        self.TYPE = 'standard'
        self.challenge_id = challenge_id
        self.content = content

        self.TYPE = kwargs['type'] if 'type' in kwargs else 'static'
        self.data = kwargs['case'] if 'case' in kwargs else None


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

        self.cost = kwargs['cost'] if 'cost' in kwargs else 0
        self.TYPE = kwargs['type'] if 'type' in kwargs else 'standard'


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
