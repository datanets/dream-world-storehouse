from bottle import post, route
from .. import dbengine
from ..app import authenticate, db_object_to_dict
from ..models import Character, Location
from ..view import render

class Characters:

    def __init__(self):
        pass

    def all(self):
        """list all characters for editing"""
        username = authenticate()
        session = dbengine.connect()

        characters = {}
        for row in session.query(Character).order_by(Character.name):
            characters[row.id] = db_object_to_dict(row)

        return render('characters/all.html', {'username': username, 'characters': characters}, 'admin.html')

    def create(self):
        """create character"""
        username = authenticate()
        session = dbengine.connect()
        locations = {}
        for location in session.query(Location):
            locations[location.id] = db_object_to_dict(location)
        return render('characters/create.html', {'username': username, 'locations': locations}, 'admin.html')

    def edit(self, id):
        """edit character"""
        username = authenticate()
        session = dbengine.connect()
        character = session.query(Character).filter(Character.id==id).first()
        locations = {}
        for location in session.query(Location):
            locations[location.id] = db_object_to_dict(location)
        return render('characters/edit.html', {'username': username, 'character': character, 'locations': locations}, 'admin.html') 

    def index(self):
        """characters index"""
        session = dbengine.connect()

        characters = {}
        for row in session.query(Character).order_by(Character.id):
            characters[row.id] = db_object_to_dict(row)

        return render('characters/index.html', {'characters': characters})

    def save(self):
        """save form content"""
        authenticate()
        session = dbengine.connect()

        id = request.forms.get('id')
        name = request.forms.get('name').decode('utf-8')
        alias = request.forms.get('alias').decode('utf-8')
        location_id = request.forms.get('location_id')

        if id:
            # update
            update = session.query(Character).get(id)
            update.name = name
            update.alias = alias
            update.location_id = location_id
        else:
            # create
            new_character = Character(name, alias, location_id)
            session.add(new_character)

        session.commit()
        redirect('/characters/all')
 
    def view(self, id):
        """character information"""
        session = dbengine.connect()

        all_characters = {}
        for row in session.query(Character).order_by(Character.id):
            all_characters[row.id] = db_object_to_dict(row)

        characters = {}
        for character in session.query(Character).\
                filter(Character.id==id).order_by(Character.id.desc()):
            characters[character.id] = character

        return render('characters/view.html', {'all_characters': all_characters, 'characters': characters})

go = Characters()
route('/characters/all')(go.all)
route('/characters/create')(go.create)
route('/characters/edit/:id')(go.edit)
route('/characters/index')(go.index)
post('/characters/save')(go.save)
route('/characters/view/:id')(go.view)
