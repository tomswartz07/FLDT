import os
from flask import Flask, render_template, redirect, request
from redis import Redis

app = Flask(__name__)
redis = Redis(host='127.0.0.1', port=6379, db=0)


@app.route("/")
def index():
    return redirect('/images')


@app.route("/api/currentImage", methods=['GET', 'POST'])
def currentImage():
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
def ImageAction():
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
# def getHostnameByMac(mac):
#     "Function to parse the mac and return hostname"
#     hostname = redis.get('mac'+mac).decode('UTF-8')
#     return hostname
def hostnamequery():
    if request.method == 'POST':
        # Do some magic to set hostname
        return 'yes'
    elif request.method == 'GET':
        # Do some magic to return hostname from Redis query
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


@app.route("/images/", methods=['GET', 'POST'])
def images(images=[]):
    # osDir is the location where the Image Files are stored
    # This can (and probably should) be modified
    global osDir
    osDir = '/home/tom'
    images = os.listdir(osDir)
#    if request.form['submit'] == 'Apply':
#        selectedImage = image
#        resp = 'You chose: ', selectedImage
#        return Response(resp)
    selectedImage = redis.get('selectedImage').decode('UTF-8')
    return render_template('index.html', images=images, osDir=osDir, selectedImage=selectedImage)


@app.route("/hosts")
@app.route("/hosts/reset")
def hosts():
    nHosts = len(redis.keys('host*'))
    hosts = redis.keys('host*')
    return render_template('hosts.html', nHosts=nHosts, hosts=hosts)


@app.route("/multicast")
def multicast(inProgress=False):
    selectedImage = redis.get('selectedImage').decode('UTF-8')
    return render_template('multicast.html', selectedImage=selectedImage, inProgress=inProgress)


# def listImages():
#     Folders = []
#     for item in os.listdir(ImagePath):
#         Folders.append(item)
#     return Folders

if __name__ == "__main__":
    app.run(port=8080, debug=True)
