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

# [START imports]
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from google.appengine.ext import ndb
# [END imports]

UPLOAD_FOLDER = '../static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# [START create_app]
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
# [END create_app]

class User(ndb.Model):
    name = ndb.StringProperty()
    major = ndb.StringProperty()
    year = ndb.StringProperty()

#LANDINGPAGE
@app.route('/')
def landing_page():
    return render_template('landingpage.html')

#BASICINFO
@app.route('/basicinfo', methods=['GET'])
def dropdown():
    return render_template('/basicinfo.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    major = request.form['major']
    year = request.form['year']
    # important
    new_entity = User(name = name, major = major, year = year)
    # will use key to query
    entity_key = new_entity.put()

    # entity_key.delete()

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        major=major,
        year=year)
    # [END render_template]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#PHOTO
# print("before photo", file=sys.stdout)

@app.route('/photo', methods=['GET', 'POST'])
def photo():
    if request.method == 'GET':
        return render_template('photo.html')
# def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     # flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # # if user does not select file, browser also
        # # submit a empty part without filename
        # if file.filename == '':
        #     # flash('No selected file')
        #     return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('photouploaded.html', file)

#FOODINFO
@app.route('/foodinfo', methods=['GET','POST'])
def food_info():
    if request.method == 'GET':
        return render_template('foodinfo.html')
    else:
        food = request.form['food']
        hobbies = request.form['hobbies']
        interests = request.form['interests']

        # important
        new_entity = User(food = food, hobbies = hobbies, interests = interests)
        # will use key to query
        entity_key = new_entity.put()

# @app.route('/submitted', methods=['POST'])
# def submitted_form():
#     name = request.form['name']
#     major = request.form['major']
#     print "hi"
#     year = request.form['year']
#     print "hello"
#
#     # important
#     new_entity = User(name = name, major = major, year = year)
#     # will use key to query
#     entity_key = new_entity.put()
#
#     # entity_key.delete()
#
#     # [END submitted]
#     # [START render_template]
#     return render_template(
#         'submitted_form.html',
#         name=name,
#         major=major,
#         year=year)

#EMAIL
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


    # to delete
    # call entity_key.delete to delete
    # query = User.query(User.preferences == user1.preference)
    # returns array, get first user, match and remove from datastore

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
