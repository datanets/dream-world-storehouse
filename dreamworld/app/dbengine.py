from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os.path import dirname
import ConfigParser

def connect():

    # get config settings
    cp = ConfigParser.ConfigParser()
    cp.read(dirname(__file__)+'/config/config.ini')

    # connect to database engine
    engine = create_engine(cp.get('db', 'engine'), echo=True)

    # bind session to database engine
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def get_engine():

    # get config settings
    cp = ConfigParser.ConfigParser()
    cp.read(dirname(__file__)+'/config/config.ini')

    # connect to database engine
    engine = create_engine(cp.get('db', 'engine'), echo=True)

    return engine
