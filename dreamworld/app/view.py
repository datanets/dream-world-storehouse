#from app import views
from bottle import route, static_file
from mako.template import Template, exceptions
from mako.lookup import TemplateLookup
from os.path import dirname

# get config settings
import ConfigParser
cp = ConfigParser.ConfigParser()
cp.read(dirname(__file__)+'/config/config.ini')

APP = cp.get('paths', 'app')
VIEWS = cp.get('paths', 'views')
LAYOUTS = cp.get('paths', 'layouts')

@route('/static/<filename:path>')
def send_static(filename):
    """get static files (css, js, etc.)"""
    return static_file(filename, root=APP+'/static')

def render(template='', values={}, layout='', typ='html'):
    """render view"""
    template_lookup = TemplateLookup(directories=[LAYOUTS])
    use_layout = "<%inherit file=\"default.html\"/>"
    if layout:
        use_layout = "<%inherit file=\"/" + layout + "\"/>"

    try:
        tf = open(VIEWS + template)
        template_as_string = tf.read()
        tf.close()
        template = Template(use_layout+template_as_string, lookup=template_lookup)
        return template.render(**values)
    except:
        return exceptions.text_error_template().render()


from views.chapter import *
from views.character import *
from views.dashboard import *
from views.homepage import *
from views.location import *
from views.passage import *
from views.user import *
