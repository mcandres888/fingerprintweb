from bottle import route, run, template, static_file, request, redirect
from struct import *
import struct
import string
import binascii
import time
import datetime
from sqldb import *


DB = SQLDatabase("finger.db")


# static files
@route('/public/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='public')


@route('/fingerprints')
def index():
    data = DB.getAllFDATA()
    print data
    return template('fingerprints', data=data)


@route('/images')
def images():
    data = DB.getAllImages()
    return template('images', data=data)

@route('/image/<epoch>/<image_path>')
def image(epoch, image_path):
    data = {
        'id' : epoch,
        'path' : image_path,
        'time' : str(datetime.datetime.fromtimestamp(float(epoch)).strftime('%c'))
    }
    return template('image', data=data)




@route('/insertImage/<image_path>')
def insertImage(image_path):
    DB.insertImage(image_path)
    data = {
        'status' : 'ok'
    }
    return data

@route('/insertActivity/<type>/<note>')
def insertActivity(type, note):
    DB.insertActivity(type, note)
    data = {
        'status' : 'ok'
    }
    return data


@route('/fingerprintupdate', method='POST')
def index():
    id = request.forms.get('finger_id')
    name = request.forms.get('finger_name')
    DB.updateFDATA(id, name)
    data = {
        'id': id,
        'name': name,
    }
    return template('fingerprintupdate', data=data)



@route('/')
def index():
    data = DB.getAllActivities()
    return template('main', data=data)

run(host='0.0.0.0', port=8095, reloader=False)

