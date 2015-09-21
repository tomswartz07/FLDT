#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import configparser
from flask import Flask, render_template, redirect, request
from redis import Redis

app = Flask(__name__)
config = configparser.RawConfigParser()
configFilePath = 'settings.cfg'
config.read(configFilePath)
redishost = config['db']['host']
redisport = config['db']['port']
redisdb = config['db']['db']
redis = Redis(host=redishost, port=redisport, db=redisdb)


@app.route("/")
def index():
    "Root webpage path, redirect to /images"
    return redirect('/images')


@app.route("/api/currentImage", methods=['GET', 'POST'])
def currentimage():
    "API to return currently selected image, used by clients during PXE install"
    global selectedImage
    if request.method == 'POST':
        current = request.args.get('set', '')
        redis.set('selectedImage', current)
        selectedImage = redis.get('selectedImage').decode('UTF-8')
        return selectedImage
    elif request.method == 'GET':
        selectedImage = redis.get('selectedImage').decode('UTF-8')
        return selectedImage
    else:
        error = 'Guru Meditation #03.01.'
        return error


@app.route("/api/postImageAction", methods=['GET', 'POST'])
def imageaction():
    "API to return currently selected post-image action, used by clients during PXE install"
    global postImageAction
    if request.method == 'POST':
        current = request.args.get('set', '')
        redis.set('postImageAction', current)
        postImageAction = redis.get('postImageAction').decode('UTF-8')
        return postImageAction
    elif request.method == 'GET':
        postImageAction = redis.get('postImageAction').decode('UTF-8')
        return postImageAction
    else:
        error = 'Guru Meditation #03.02'
        return error


@app.route("/api/hostname", methods=['GET', 'POST'])
def hostnamequery():
    "API to return hostname based upon MAC address, used by clients during PXE install"
    if request.method == 'POST':
        # Do some magic to set hostname, maybe?
        return 'yes'
    elif request.method == 'GET':
        try:
            current = request.args.get('mac', '')
            hostname = redis.get('mac'+current).decode('UTF-8')[4:]
            return hostname
        except Exception:
            # The host is unknown, so set hostname as such
            error = 'unknown'
            return error
    else:
        error = 'Guru Meditation #03.03'
        return error
# def getHostnameByMac(mac):
#     "Function to parse the mac and return hostname"
#     hostname = redis.get('mac'+mac).decode('UTF-8')
#     return hostname


@app.route("/images/", methods=['GET', 'POST'])
def images(images=['']):
    global osDir
    osDir = config['setup']['imagepath']
    images = os.listdir(osDir)
    return render_template('index.html', images=images, osDir=osDir)


@app.route("/hosts", methods=['GET', 'POST'])
# @app.route("/hosts/reset")
def hosts():
    "Defines the Host page functions"
    hosts = redis.keys('host*')
    macs = redis.keys('mac*')
    nHosts = len(hosts)
    clients = zip(hosts, macs)
    if request.method == 'POST':
        hostcsv = request.files.get['file']
        if hostcsv and allowed_file(hostcsv.filename):
            return hostcsv
    return render_template('hosts.html', nHosts=nHosts, clients=clients)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'csv'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def process_csv_file(csv_file):
    "Process the csv file and add it to the DB"
    # Work in progress
    with open(csv_file) as f:
        host = csv.reader(f)
        for row in host:
            print(row)
    return host


@app.route("/multicast", methods=['GET', 'POST'])
def multicast(inProgress=False, minClients=10):
    "Configures the MulticastManager Processes"
    import subprocess
    try:
        inProgress = redis.get('inProgress').decode('UTF-8')
    except AttributeError:
        redis.set('inProgress', False)
        inProgress = redis.get('inProgress').decode('UTF-8')
    try:
        selectedImage = redis.get('selectedImage').decode('UTF-8')
    except AttributeError:
        redis.set('selectedImage', 'Not Selected')
        inProgress = redis.get('selectedImage').decode('UTF-8')
    try:
        postImageAction = redis.get('postImageAction').decode('UTF-8')
    except AttributeError:
        redis.set('postImageAction', 'shell')
        postImageAction = redis.get('postImageAction').decode('UTF-8')
    cmd = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE, shell=True)
    pid = cmd.pid
    if request.method == 'POST':
        current = request.args.get('inProgress', '')
        minClients = request.args.get('autostart', '')
        redis.set('inProgress', current)
        return redirect('/multicast')
#    elif request.method == 'GET':
#        postImageAction = redis.get('postImageAction').decode('UTF-8')
#        return postImageAction
#    else:
#        error = 'Guru Meditation #03.02'
#        return error
    return render_template('multicast.html', minClients=minClients,
                           pid=pid, selectedImage=selectedImage,
                           inProgress=inProgress, postImageAction=postImageAction)


# def listImages():
#     Folders = []
#     for item in os.listdir(ImagePath):
#         Folders.append(item)
#     return Folders

if __name__ == "__main__":
    serverport = int(config['setup']['http_port'])
    app.run(port=serverport, debug=True)
