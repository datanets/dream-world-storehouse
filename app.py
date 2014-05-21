from bottle import redirect, request
from os.path import dirname
import ConfigParser

def authenticate():
    """check if a user is logged in"""
    try:
        beaker_session = request.environ['beaker.session']
        username = beaker_session['username']
        return username
    except:
        redirect('/users/login')

def db_object_to_dict(row):
    """
    turn custom database table object into a dict
    so it can be sorted in template
    """
    return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())

def get_config():
    """get config file"""
    cp = ConfigParser.ConfigParser()
    cp.read(dirname(__file__)+'/config/config.ini')
    return cp
