#!/usr/bin/env python

from app import app
import os
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from camera_opencv import Camera
import time
from datetime import datetime
import flow_monitor
import numpy as np
from threading import Thread

flowthread=Thread()
pressurethread=Thread()

socketio = SocketIO(app)

uport = 0
dport = 0

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/people')
def people():
    return render_template('people.html', title='People')

@app.route('/frictionlab')
def frictionlab():
    """Video streaming home page."""
    timeNow = time.asctime( time.localtime(time.time()) )
    templateData = {
        'time': timeNow
    }
    return render_template('frictionlab.html', title='Friction Lab')

class FlowThread(Thread):
    """Stream data on thread"""
    def __init__(self):
        self.delay = 1
        super(FlowThread, self).__init__()

    def get_data(self):
        """Get data and emit to socket"""
        flowrate = 0
        while True:
            flowrate = round(np.random.random(),3)
            socketio.emit('flowrate',{'flowrate': flowrate}, namespace='/flowrate_socket')
            time.sleep(self.delay)

    def run(self):
        """Default run method"""
        self.get_data()

class PressThread(Thread):
    """Stream data on thread"""
    def __init__(self):
        self.delay = 1
        super(PressThread, self).__init__()
    
    def get_data(self):
        """Get data and emit to socket"""
        pressure1=0
        pressure2=0
        while True:
            socketio.emit('pressure1',{'pressure1': pressure1, 'pressure2': pressure2}, namespace='/pressure1_socket')
            pressure1 = uport
            pressure2 = dport
            time.sleep(self.delay)

    def run(self):
        """Default run method"""
        self.get_data()

@socketio.on('connect', namespace='/flowrate_socket')
def connect_socket():
    """Handle socket connection"""
    global flowthread

    # Start thread
    if not Thread.isAlive(flowthread):
        flowthread = FlowThread()
        flowthread.start()

@socketio.on('connect', namespace='/pressure1_socket')
def connect_socket():
    """Handle socket connection"""
    global pressurethread
    
    # Start thread
    if not Thread.isAlive(pressurethread):
        pressurethread = PressThread()
        pressurethread.start()

@socketio.on('uport', namespace='/pressure1_socket')
def read_uport(json):
    global uport
    uport = json

@socketio.on('dport', namespace='/pressure1_socket')
def read_dport(json):
    global dport
    dport = json

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    socketio.run(app)
#app.run(host='0.0.0.0', threaded=True)

