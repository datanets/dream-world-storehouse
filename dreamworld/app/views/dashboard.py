from bottle import get, post, redirect, request, route
from .. import app
from ..app import authenticate, db_object_to_dict
from ..view import render

class Dashboard:

    def __init__(self):
        pass

    def index(self):
        """dashboard index"""
        username = authenticate()
        return render('dashboard/index.html', {'username': username}, 'admin.html')

go = Dashboard()
route('/dashboard/index')(go.index)
