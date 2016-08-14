from bottle import route, run, template, static_file, request, redirect
from struct import *
import struct
import string
import binascii
import time
import datetime


# static files
@route('/public/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='public')



@route('/')
def index():
    data = {
        'unregistered' : "test"
    }
    return template('main', data=data)

run(host='0.0.0.0', port=8094, reloader=True)

