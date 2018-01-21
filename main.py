# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
import os
import base64
import cloudstorage as gcs
import io

# [START imports]
from flask import Flask, render_template, request, send_file
from google.appengine.ext import ndb
from google.appengine.api import app_identity
# [END imports]

UPLOAD_FOLDER = './img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# [START create_app]
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# [END create_app]

class User(ndb.Model):
    name = ndb.StringProperty()
    major = ndb.StringProperty()
    year = ndb.StringProperty()
    photo = ndb.BlobProperty()
    user_id = ndb.IntegerProperty()

#LANDINGPAGE
@app.route('/')
def landing_page():
    return render_template('landingpage.html')

#BASICINFO
@app.route('/basicinfo', methods=['GET'])
def dropdown():
    return render_template('/basicinfo.html')


@app.route('/basicinfo', methods=['POST'])
def submitted_form():
    name = request.form['name']
    major = request.form['major']
    year = request.form['year']

    # important
    new_entity = User(name = name, major = major, year = year)
    # will use key to query
    entity_key = new_entity.put()
    print entity_key
    # entity_key.delete()

    # [END submitted]
    # [START render_template]
    return render_template(
        'photo.html', entity_key=entity_key.urlsafe())
    # [END render_template]

@app.route('/photo', methods=['GET'])
def get_photo():
    return render_template('photo.html')

@app.route('/photo', methods=['POST'])
def upload_photo():
    photo = request.files['photo']
    entity_key = request.form['entity_key']
    if entity_key:
        print entity_key
        print "I got the entity"
    else:
        print "hi"
    new_key = ndb.Key(urlsafe=entity_key)
    user = new_key.get()
    print user.name
    #user.photo = ndb.Blob(photo)
    print type(user)
    print type(photo)
    # user.photo = base64.b64encode(photo.read()).decode('UTF-8')
    # print type(user.photo)
    # user.put()
    bucket_name = 'tomeeto-hackdavis.appspot.com';
    #app_identity.get_default_gcs_bucket_name()
    print bucket_name
    filename = '/' + bucket_name + '/' + photo.filename

    gcs_file = gcs.open(filename, 'w')
    gcs_file.write(photo.read())
    gcs_file.close()

    gcs_file = gcs.open(filename)
    contents = gcs_file.read()
    gcs_file.close()


    return render_template(
        'displayphoto.html',
        bucket_name=bucket_name,
        img_name=photo.filename
    )
    # return send_file(io.BytesIO(contents),
    #                mimetype='image/jpeg')

@app.route('/displayphoto', methods=['GET'])
def get_displayphoto():
    return render_template("displayphoto.html")

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#PHOTO
# @app.route('/photo', methods=['GET', 'POST'])
# def photo():
#     return render_template('/photo.html')
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     return render_template('photo.html')

#FOODINFO
@app.route('/foodinfo', methods=['GET'])
def foodinfo():
    return(render_template('foodinfo.html'))
    # [END render_template]


    # to delete
    # call entity_key.delete to delete
    # query = User.query(User.preferences == user1.preference)
    # returns array, get first user, match and remove from datastore
@app.route('/email', methods=['GET','POST'])
def email():
    if request.method == 'GET':
        return render_template('email.html')
    if request.method == 'POST':
        email = request.form['email']
        # important
        new_entity = User(email = email)
        # will use key to query
        entity_key = new_entity.put()


@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
