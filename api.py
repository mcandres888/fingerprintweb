from bottle import route, run, template, static_file, request, redirect
import bottle
from struct import *
import struct
import string
import binascii
import time
import datetime
from sqldb import *
from subprocess import call
import requests


app = application = bottle.Bottle()
DB = SQLDatabase("finger.db")

def getTimeStampFileName ():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d%H_%M_%S.jpg')
    return st

def takesnapshot():
    requests.get("http://localhost:8082/0/action/snapshot")
    # copy file to images folder
    filename = getTimeStampFileName() 
    filepath = "/home/pi/sandbox/fingerprintweb/public/images/%s" % filename 
    call(["cp", "/tmp/motion/lastsnap.jpg", filepath])
    return filename


def getLocalVariables () :
    localData = {}
    host = request.get_header('host')
    localData['host'] = host
    return localData


# static files
@app.route('/public/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='public')


@app.route('/snapshot')
def snapshot():
    filename = takesnapshot()
    DB.insertImage(filename)
    redirect('/')


@app.route('/fingerprints')
def index():
    data = DB.getAllFDATA()
    localData = getLocalVariables()
    localData['data'] = data
    return template('fingerprints', data=localData)


@app.route('/images')
def images():
    data = DB.getAllImages()
    localData = getLocalVariables()
    localData['data'] = data
    return template('images', data=localData)

@app.route('/image/<epoch>/<image_path>')
def image(epoch, image_path):
    data = {
        'id' : epoch,
        'path' : image_path,
        'time' : str(datetime.datetime.fromtimestamp(float(epoch)).strftime('%c'))
    }
    return template('image', data=data)

@app.route('/image/delete/<epoch>/<image_path>')
def image(epoch, image_path):
    call(["rm", "/home/pi/sandbox/fingerprintweb/public/images/%s" % image_path])
    DB.deleteImage(epoch)
    redirect('/images')






@app.route('/insertImage/<image_path>')
def insertImage(image_path):
    DB.insertImage(image_path)
    data = {
        'status' : 'ok'
    }
    return data

@app.route('/insertActivity/<type>/<note>')
def insertActivity(type, note):
    DB.insertActivity(type, note)
    data = {
        'status' : 'ok'
    }
    return data


@app.route('/fingerprintupdate', method='POST')
def index():
    id = request.forms.get('finger_id')
    name = request.forms.get('finger_name')
    DB.updateFDATA(id, name)
    data = {
        'id': id,
        'name': name,
    }
    localData = getLocalVariables()
    localData['data'] = data
    return template('fingerprintupdate', data=localData)



@app.route('/')
def index():
    data = DB.getAllActivities()
    localData = getLocalVariables()
    localData['data'] = data
    return template('main', data=localData)

class StripPathMiddleware(object):
    '''
    Get that slash out of the request
    '''
    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

if __name__ == '__main__':
    bottle.run(app=StripPathMiddleware(app),
        host='0.0.0.0',
        port=8095)
