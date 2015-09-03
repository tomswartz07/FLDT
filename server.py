#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import configparser
from flask import Flask, render_template, redirect, request
from redis import Redis

app = Flask(__name__)
redis = Redis(host='127.0.0.1', port=6379, db=0)
config = configparser.RawConfigParser()
configFilePath = 'settings.cfg'
config.read(configFilePath)


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
            hostname = redis.get('mac'+current).decode('UTF-8')
            return hostname
        except:
            error = 'Unknown Mac Address Request'
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


@app.route("/hosts")
@app.route("/hosts/reset")
def hosts():
    "Defines the Host page functions"
    hosts = redis.keys('host*')
    macs = redis.keys('mac*')
    nHosts = len(hosts)
    return render_template('hosts.html', nHosts=nHosts, hosts=hosts, macs=macs)


@app.route("/multicast")
def multicast(inProgress=False):
    selectedImage = redis.get('selectedImage').decode('UTF-8')
    postImageAction = redis.get('postImageAction').decode('UTF-8')
    return render_template('multicast.html', selectedImage=selectedImage, inProgress=inProgress, postImageAction=postImageAction)


# def listImages():
#     Folders = []
#     for item in os.listdir(ImagePath):
#         Folders.append(item)
#     return Folders

if __name__ == "__main__":
    app.run(port=8080, debug=True)
