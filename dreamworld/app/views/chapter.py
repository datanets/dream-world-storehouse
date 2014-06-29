from bottle import get, post, redirect, request, route
from .. import app
from .. import dbengine
from ..app import authenticate, db_object_to_dict
from ..models import Chapter, Character, Passage
from ..view import render

class Chapters:

    def __init__(self):
        pass

    def all(self):
        """list all chapters for editing"""
        username = authenticate()
        session = dbengine.connect()

        chapters = {}
        for row in session.query(Chapter).order_by(Chapter.chapter_order):
            chapters[row.id] = db_object_to_dict(row)

        return render('chapters/all.html', {'username': username, 'chapters': chapters}, 'admin.html')

    def create(self):
        """create chapter"""
        username = authenticate()
        chapter_order = range(1,100)
        return render('chapters/create.html', {'username': username, 'chapter_order': chapter_order}, 'admin.html')

    def edit(self, id):
        """edit chapter"""
        username = authenticate()
        session = dbengine.connect()
        chapter = session.query(Chapter).filter(Chapter.id==id).first()
        chapter_order = range(1,100)
        cp = app.get_config()
        splash_images_url = cp.get('paths', 'splash_images_url')
        return render('chapters/edit.html',
                {
                    'chapter': chapter,
                    'chapter_order': chapter_order,
                    'splash_images_url': splash_images_url,
                    'username': username
                },
                'admin.html'
            )

    def index(self):
        """chapter index"""
        session = dbengine.connect()

        chapters = {}
        for row in session.query(Chapter).order_by(Chapter.id):
            chapters[row.id] = db_object_to_dict(row)

        return render('chapters/index.html', {'chapters': chapters})

    def save(self):
        """save form content"""
        authenticate()
        session = dbengine.connect()

        cp = app.get_config()
        splash_images_dir = cp.get('paths', 'splash_images_dir')

        id = request.forms.get('id')
        name = request.forms.get('name').decode('utf-8')
        chapter_order = request.forms.get('chapter_order')
        splash_image = request.files.get('splash_image')
        audio_link = request.forms.get('audio_link')

        if id:
            # update
            update = session.query(Chapter).get(id)
            update.name = name
            update.chapter_order = chapter_order
            # if new splash image
            if splash_image is not None:
                if update.splash_image != splash_image.filename:
                    update.splash_image = splash_image.filename
                    if splash_image and splash_image.file and splash_image.filename:
                        raw = splash_image.file.read()  # dangerous for big files
                        save_file = open(splash_images_dir + splash_image.filename, 'w')
                        save_file.write(raw)
                        save_file.close()
            update.audio_link = audio_link
        else:
            # create
            new_chapter = Chapter(name, chapter_order, splash_image.filename, audio_link)
            if splash_image and splash_image.file and splash_image.filename:
                raw = splash_image.file.read()  # dangerous for big files
                save_file = open(splash_images_dir + splash_image.filename, 'w')
                save_file.write(raw)
                save_file.close()
            session.add(new_chapter)

        session.commit()
        redirect('/chapters/index')

    def view(self, id):
        """chapter information"""
        session = dbengine.connect()

        chapters = {}
        for chapter in session.query(Chapter).\
                filter(Chapter.id==id).order_by(Chapter.id):
            chapters[chapter.id] = chapter

        all_chapters = {}
        for row in session.query(Chapter).order_by(Chapter.id):
            all_chapters[row.id] = db_object_to_dict(row)

        characters = {}
        for row in session.query(Character).order_by(Character.id):
            characters[row.id] = db_object_to_dict(row)

        passages = {}
        for row in session.query(Passage).\
                filter(Passage.chapter_id==id).order_by(Passage.passage_order):
            row.body = '<br />'.join(row.body.splitlines())
            passages[row.id] = db_object_to_dict(row)

        cp = app.get_config()
        splash_images_url = cp.get('paths', 'splash_images_url')

        return render('chapters/view.html', {'all_chapters': all_chapters, 'chapters': chapters, 'characters': characters, 'passages': passages, 'splash_images_url': splash_images_url})

go = Chapters()
route('/chapters/all')(go.all)
route('/chapters/create')(go.create)
route('/chapters/edit/:id')(go.edit)
route('/chapters/index')(go.index)
post('/chapters/save')(go.save)
route('/chapters/view/:id')(go.view)
