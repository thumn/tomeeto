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
from flask import Flask, render_template, request
from google.appengine.ext import ndb
# [END imports]

UPLOAD_FOLDER = './img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# [START create_app]
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# [END create_app]


class User(ndb.Model):
    username = ndb.StringProperty()
    email = ndb.StringProperty()

#LANDINGPAGE
@app.route('/')
def landing_page():
    return render_template('landingpage.html')

#BASICINFO
@app.route('/basicinfo', methods=['GET'])
def dropdown():
    years = ['Freshman','Sophomore','Junior','Senior','Super Senior!!11!!'];
    return render_template('/basicinfo.html', years=years)

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#PHOTO
@app.route('/photo', methods=['GET', 'POST'])
def photo():
    return render_template('/photo.html')
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
# @app.route('/foodinfo', methods=['POST'])
# def submitted_form():
#     name = request.form['name']
#     email = request.form['email']
#     site = request.form['site_url']
#     comments = request.form['comments']
#
#     # important
#     new_entity = User(username = name, email = email)
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
#         email=email,
#         site=site,
#         comments=comments)
    #[END render_template]

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
