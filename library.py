import time
import errno
from socket import error as socket_error
import json
import socket
import datetime
import binascii
import os

import requests

CARD_CHECK = "http://192.168.1.252:20000/api/vend-card"
HOST = "192.168.1.252"
PORT = 20000

def checkCard (rfid, node, price):
    if node == 7:
        machine_name = "DRY%d" % int(node)
    else:
        machine_name = "MAC%d" % int(node)
    data = {
        "branch_id": "4",
        "card_code": rfid,
        "machine_name": machine_name,
        "machine_load": "%d" % price
    }
    data_s = '[{ "card_code" : "' + rfid + '", '
    data_s +='"machine_load" : ' + str(price) + ', '
    data_s +='"machine_name" : "' + machine_name + '", '
    data_s +='"branch_id" : "4" }]'

    print "sending data", data
    infoLog("sending data to %s" % CARD_CHECK)
    infoLog("    branch_id = %s" % data['branch_id'])
    infoLog("    card_code = %s" % data['card_code'])
    infoLog("    machine_name = %s" % data['machine_name'])
    infoLog("    machine_load = %s" % data['machine_load'])

    #SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #SOCK.connect((HOST,PORT))
    #SOCK.send(data_s.encode())
    #data, addr = SOCK.recvfrom(1024)
    #print "recv_data : ", data
    #SOCK.close()
    #json_data  = json.loads(data)
    json_data = sendToSocket ( data_s , 5 ) 
    infoLog("response data from %s" % CARD_CHECK)
    infoLog("    status = %s" % json_data['status'])
    if json_data['status'] == 0:
        infoLog("    message = %s" % json_data['message'])

    return json_data['status']


def checkCard3 (rfid, node, price):
    json_data = {}
    #json_data['status'] = 1
    #return json_data
    if node == 7:
        machine_name = "DRY%d" % int(node)
    else:
        machine_name = "MAC%d" % int(node)
    data = {
        "branch_id": "4",
        "card_code": rfid,
        "machine_name": machine_name,
        "machine_load": "%d" % price
    }
    data_s = '[{ "card_code" : "' + rfid + '", '
    data_s +='"machine_load" : ' + str(price) + ', '
    data_s +='"machine_name" : "' + machine_name + '", '
    data_s +='"branch_id" : "4" }]'

    print "sending data", data
    infoLog("sending data to %s" % CARD_CHECK)
    infoLog("    branch_id = %s" % data['branch_id'])
    infoLog("    card_code = %s" % data['card_code'])
    infoLog("    machine_name = %s" % data['machine_name'])
    infoLog("    machine_load = %s" % data['machine_load'])

    #SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #SOCK.connect((HOST,PORT))
    #SOCK.send(data_s.encode())
    #data, addr = SOCK.recvfrom(1024)
    #print "recv_data : ", data
    #SOCK.close()
    #json_data  = json.loads(data)
    json_data = sendToSocket ( data_s , 5 ) 
    infoLog("response data from %s" % CARD_CHECK)
    infoLog("    status = %s" % json_data['status'])
    if json_data['status'] == 0:
        infoLog("    message = %s" % json_data['message'])

    return json_data



def checkCardDryer (rfid, node, price):
    #return 1
    machine_name = "DRY%d" % int(node)
    data = {
        "branch_id": "4",
        "card_code": rfid,
        "machine_name": machine_name,
        "machine_load": "%d" % price
    }
    data_s = '[{ "card_code" : "' + rfid + '", '
    data_s +='"machine_load" : ' + str(price) + ', '
    data_s +='"machine_name" : "' + machine_name + '", '
    data_s +='"branch_id" : "4" }]'

    print "sending data", data
    infoLog("sending data to %s" % CARD_CHECK)
    infoLog("    branch_id = %s" % data['branch_id'])
    infoLog("    card_code = %s" % data['card_code'])
    infoLog("    machine_name = %s" % data['machine_name'])
    infoLog("    machine_load = %s" % data['machine_load'])

    infoLog("sending data from %s" % HOST)
    json_data = sendToSocket ( data_s , 5 )
    infoLog("response data from %s" % HOST)
    infoLog("    status = %s" % json_data['status'])
    if json_data['status'] == 0:
        infoLog("    message = %s" % json_data['message'])
        return 0

    return json_data['vendload']




def sendToSocket ( data_s , retry ) :

    json_data = {}
    json_data['status'] = 0
    json_data['message'] = "socket retry count reached"
    try:
        SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SOCK.connect(("192.168.1.252",20000))
        SOCK.send(data_s.encode())
        data, addr = SOCK.recvfrom(1024)
        print "recv_data : ", data
        SOCK.close()
        json_data  = json.loads(data)
        return json_data
    except socket_error as serr:           
        infoLog("Socket error, retrying %d" %  retry)
        if retry == 0:
            return json_data
        else:
            json_data = sendToSocket(data_s, retry - 1)
            return json_data


    

    

def checkCard2 (rfid, node, price):
    if node == 7:
        machine_name = "DRY%d" % int(node)
    else:
        machine_name = "MAC%d" % int(node)
    data = {
        "branch_id": "4",
        "card_code": rfid,
        "machine_name": machine_name,
        "machine_load": "%d" % price
    }
    print "sending data", data
    infoLog("sending data to %s" % CARD_CHECK)
    infoLog("    branch_id = %s" % data['branch_id'])
    infoLog("    card_code = %s" % data['card_code'])
    infoLog("    machine_name = %s" % data['machine_name'])
    infoLog("    machine_load = %s" % data['machine_load'])
    response = requests.post(CARD_CHECK,params=data)
    json_data = response.json()
    infoLog("response data from %s" % CARD_CHECK)
    infoLog("    status = %s" % json_data['status'])
    if json_data['status'] == 0:
        infoLog("    message = %s" % json_data['message'])

    return json_data['status']
    



def getTimeStamp ():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
 
    #now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    return st


def infoLog ( data ):
    st = getTimeStamp()
    os.system("echo '[%s]%s'" % (st,data))

def convertToCharData ( packet):
    packet_split = packet.split(":")
    char_data = ""
    for p in packet_split:
        i = chr(int(p,16))
        char_data += i
    return char_data


def convertHexToInt (data):
    temp = data.split(":")
    hex_string = ''.join(temp)
    rfid = int(hex_string, 16)
    return rfid

def getRfid ( data ):
    recv_data = ':'.join( binascii.hexlify(x).upper()  for x in data)
    rfid = 0
    if len(recv_data) == 11:
        # this is an rfid
        rfid = convertHexToInt (recv_data)
    return rfid


def replyNodeDryer ( addr, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((addr, 54889))
    s.send(data)
    s.close()



def replyNode ( addr, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((addr, 64889))
    s.send(data)
    s.close()


rfid = "400675E5A"
node = 4
price = 30
#checkCard(rfid, node, price)



