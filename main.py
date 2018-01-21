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

# [START imports]
from flask import Flask, render_template, request
from google.appengine.ext import ndb
# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]

class User(ndb.Model):
    name = ndb.StringProperty()
    major = ndb.StringProperty()
    year = ndb.StringProperty()

@app.route('/')
def landing_page():
    return render_template('landingpage.html')

@app.route('/basicinfo', methods=['GET'])
def dropdown():
    years = ['Freshman','Sophomore','Junior','Senior','Super Senior!!11!!'];
    return render_template('/basicinfo.html', years=years)

@app.route('/submitted', methods=['POST'])
def submitted_form():
    print "hello"
    name = request.form['name']
    major = request.form['major']
    print "hi"
    # year = request.form['year']

    # important
    new_entity = User(name = name, major = major)
    # will use key to query
    entity_key = new_entity.put()

    # entity_key.delete()

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        major=major)
    # [END render_template]

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
