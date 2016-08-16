from bottle import route, run, template, static_file, request, redirect
from struct import *
import struct
import string
import binascii
import time
import datetime
from sqldb import *
from subprocess import call
import requests


DB = SQLDatabase("finger.db")

def getTimeStampFileName ():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d%H_%M_%S.jpg')
    return st

def takesnapshot():
    requests.get("http://localhost:8082/0/action/snapshot")
    # copy file to images folder
    filename = getTimeStampFileName() 
    filepath = "/home/mcandres/sandbox/fingerprintweb/public/images/%s" % filename 
    call(["cp", "/tmp/motion/lastsnap.jpg", filepath])
    return filename


def getLocalVariables () :
    localData = {}
    host = request.get_header('host')
    localData['host'] = host
    return localData


# static files
@route('/public/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='public')


@route('/snapshot')
def snapshot():
    takesnapshot()
    redirect('/')


@route('/fingerprints')
def index():
    data = DB.getAllFDATA()
    localData = getLocalVariables()
    localData['data'] = data
    return template('fingerprints', data=localData)


@route('/images')
def images():
    data = DB.getAllImages()
    localData = getLocalVariables()
    localData['data'] = data
    return template('images', data=localData)

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
    localData = getLocalVariables()
    localData['data'] = data
    return template('fingerprintupdate', data=localData)



@route('/')
def index():
    data = DB.getAllActivities()
    localData = getLocalVariables()
    localData['data'] = data
    return template('main', data=localData)

run(host='0.0.0.0', port=8095, reloader=False)

