from bottle import route
from .. import dbengine
from ..app import db_object_to_dict
from ..models import Chapter, Character, Location
from ..view import render

class Homepage:

    def __init__(self):
        pass

    def index(self):
        """show homepage"""
        session = dbengine.connect()

        chapters = {}
        for row in session.query(Chapter).order_by(Chapter.id):
            chapters[row.id] = db_object_to_dict(row)

        characters = {}
        for row in session.query(Character).order_by(Character.id):
            characters[row.id] = db_object_to_dict(row)

        locations = {}
        for row in session.query(Location).order_by(Location.id.desc()):
            locations[row.id] = db_object_to_dict(row)

        return render('homepage/index.html', {'chapters': chapters, 'characters': characters, 'locations':locations})


go = Homepage()
route('/')(go.index)
