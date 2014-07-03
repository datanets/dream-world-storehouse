from bottle import abort, get, post, redirect, request, route
from .. import dbengine
from ..app import authenticate, db_object_to_dict
from ..models import Chapter, Character, Passage
from ..view import render

class Passages:

    def __init__(self):
        pass

    def all(self):
        """list all passages for editing"""
        username = authenticate()
        session = dbengine.connect()

        passages = {}
        for row in session.query(Passage).order_by(Passage.chapter_id).\
                order_by(Passage.passage_order):
            passages[row.id] = db_object_to_dict(row)

        return render('passages/all.html', {'passages': passages, 'username': username}, 'admin.html')

    def create(self):
        """create passage"""
        username = authenticate()
        session = dbengine.connect()

        chapters = {}
        for chapter in session.query(Chapter):
            chapters[chapter.id] = db_object_to_dict(chapter)

        characters = {}
        for character in session.query(Character):
            characters[character.id] = db_object_to_dict(character)

        passage_order = range(1,100)

        return render('passages/create.html',
                {
                    'chapters': chapters,
                    'characters': characters,
                    'passage_order': passage_order,
                    'username': username
                },
                'admin.html'
            ) 

    def edit(self, id):
        """edit passage"""
        username = authenticate()
        session = dbengine.connect()

        chapters = {}
        for chapter in session.query(Chapter):
            chapters[chapter.id] = db_object_to_dict(chapter)

        characters = {}
        for character in session.query(Character):
            characters[character.id] = db_object_to_dict(character)

        passage = session.query(Passage).filter(Passage.id==id).first()

        passage_order = range(1,100)

        return render('passages/edit.html',
                {
                    'chapters': chapters,
                    'characters': characters,
                    'passage': passage,
                    'passage_order': passage_order,
                    'username': username
                },
                'admin.html'
            ) 

    def save(self):
        """save form content"""
        authenticate()
        session = dbengine.connect()

        id = request.forms.get('id')
        body = request.forms.get('body').decode('utf-8')
        character_id = request.forms.get('character_id')
        chapter_id = request.forms.get('chapter_id')
        passage_order = request.forms.get('passage_order')
        soliloquy = request.forms.get('soliloquy')

        if id:
            # update
            update = session.query(Passage).get(id)
            update.body = body
            update.character_id = character_id
            update.chapter_id = chapter_id
            update.passage_order = passage_order
            update.soliloquy = soliloquy
        else:
            # create
            new_passage = Passage(body, character_id, chapter_id, passage_order, soliloquy)
            session.add(new_passage)

        session.commit()
        redirect('/passages/all')

    def view(self, id):
        """passage information"""
        session = dbengine.connect()

        passages = {}
        for passage in session.query(Passage).\
                filter(Passage.id==id).order_by(Passage.id.desc()):
            passages[passage.id] = passage

        return render('passages/view.html', {'passages': passages})

go = Passages()
route('/passages/all')(go.all)
route('/passages/create')(go.create)
route('/passages/edit/:id')(go.edit)
post('/passages/save')(go.save)
route('/passages/view/:id')(go.view)
