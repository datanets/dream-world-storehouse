from bottle import post, route
from .. import dbengine
from ..app import authenticate, db_object_to_dict
from ..models import Location
from ..view import render

class Locations:

    def __init__(self):
        pass

    def all(self):
        """list all locations for editing"""
        username = authenticate()
        session = dbengine.connect()

        locations = {}
        for row in session.query(Location).order_by(Location.name):
            locations[row.id] = db_object_to_dict(row)

        return render('locations/all.html', {'username': username, 'locations': locations}, 'admin.html')

    def create(self):
        """create location"""
        username = authenticate()
        session = dbengine.connect()
        return render('locations/create.html', {'username': username}, 'admin.html')

    def edit(self, id):
        """edit location"""
        username = authenticate()
        session = dbengine.connect()
        location = session.query(Location).filter(Location.id==id).first()
        return render('locations/edit.html', {'location': location, 'username': username}, 'admin.html') 

    def save(self):
        """save form content"""
        authenticate()
        session = dbengine.connect()

        id = request.forms.get('id')
        name = request.forms.get('name').decode('utf-8')

        if id:
            # update
            update = session.query(Location).get(id)
            update.name = name
        else:
            # create
            new_location = Location(name)
            session.add(new_location)

        session.commit()
        redirect('/locations/all')

    def index(self):
        """locations index"""
        session = dbengine.connect()

        locations = {}
        for row in session.query(Location).order_by(Location.id):
            locations[row.id] = db_object_to_dict(row)

        return render('locations/index.html', {'locations': locations})

    def view(self, id):
        """location information"""
        session = dbengine.connect()

        all_locations = {}
        for row in session.query(Location).order_by(Location.id.desc()):
            all_locations[row.id] = db_object_to_dict(row)

        locations = {}
        for location in session.query(Location).\
                filter(Location.id==id).order_by(Location.id.desc()):
            locations[location.id] = location

        return render('locations/view.html', {'all_locations': all_locations, 'locations': locations})

go = Locations()
route('/locations/all')(go.all)
route('/locations/create')(go.create)
route('/locations/edit/:id')(go.edit)
route('/locations/index')(go.index)
post('/locations/save')(go.save)
route('/locations/view/:id')(go.view)
