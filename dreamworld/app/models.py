from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, backref
from dbengine import get_engine

# for database connection
Base = declarative_base()

class Chapter(Base):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    chapter_order = Column(Integer)
    splash_image = Column(String)
    audio_link = Column(String)

    def __init__(self, name, chapter_order, splash_image, audio_link):
        self.name = name
        self.chapter_order = chapter_order
        self.splash_image = splash_image
        self.audio_link = audio_link

    def get(self, column):
        return getattr(self, column)

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    alias = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id"))
    gender = Column(String)
    color = Column(String)
    background_color = Column(String)

    location = relationship("Location", backref="character", primaryjoin="Character.location_id==Location.id", uselist=False)

    def __init__(self, name, alias, location_id, gender, color, background_color):
        self.name = name
        self.alias = alias
        self.location_id = location_id
        self.gender = gender
        self.color = color
        self.background_color = background_color

    def get(self, column):
        return getattr(self, column)

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    alias = Column(String)
    description = Column(Text)

    def __init__(self, name, alias, description):
        self.name = name
        self.alias = alias
        self.description = description

    def get(self, column):
        return getattr(self, column)

class Passage(Base):
    __tablename__ = 'passages'

    id = Column(Integer, primary_key=True)
    body = Column(Text)
    character_id = Column(Integer, ForeignKey("characters.id"))
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    passage_order = Column(Integer)
    soliloquy = Column(Boolean)

    character = relationship("Character", backref="passage", primaryjoin="Passage.character_id==Character.id", uselist=False)
    chapter = relationship("Chapter", backref="passage", primaryjoin="Passage.chapter_id==Chapter.id", uselist=False)

    def __init__(self, body, character_id, chapter_id, passage_order, soliloquy):
        self.body = body
        self.character_id = character_id
        self.chapter_id = chapter_id
        self.passage_order = passage_order
        self.soliloquy = soliloquy

    def get(self, column):
        return getattr(self, column)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get(self, column):
        return getattr(self, column)


# create tables if necessary
engine = get_engine()
Base.metadata.create_all(engine)
