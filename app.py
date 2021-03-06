from datetime import datetime
from flask import Flask, make_response, render_template, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = os.environ['MONGO_URI']
mongo = PyMongo(app)


@app.route('/')
def index():
	return '<h1>Maven Reaction Web Server</h1>'

@app.route('/issues', methods=['GET', 'POST'])
def handle_issues():
	if request.method == 'GET':
		return show_issues()
	else:
		
		return add_issue(request.form)

def add_issue(form):
	issues = mongo.db.issues
	issue = {
		'groupId': form['groupId'],
		'artifactId': form['artifactId'],
		'v1': form['v1'],
		'v2': form['v2'],
		'detectionId': form['detectionId'],
		'bc': form['bc'],
		'use': form['use'],
		'rangeId': form['rangeId'],
		'reviewer': form['reviewer'],
		'description': form['description'],
		'emptyDiff': form['emptyDiff'],
		'validDetection': form['validDetection'],
		'sliceNoise': form['sliceNoise'],
		'sliceRelevance': form['sliceRelevance'],
		'timestamp': datetime.now().timestamp()
	}
	issues.insert_one(issue)
	response = make_response()
	response.status_code = 201
	return response

def show_issues():
	col_issues = mongo.db.issues
	issues = col_issues.find()
	modif_issues = list()
	api = get_api_info()
	
	for issue in issues:
		issue['date'] = str(datetime.fromtimestamp(issue['timestamp']))
		modif_issues.append(issue)

	return render_template('feedback.html', issues=modif_issues, api=api)

def get_api_info():
	col_issues = mongo.db.issues
	issue = col_issues.find_one()

	api = dict()
	api['groupId'] = issue['groupId']
	api['artifactId'] = issue['artifactId']
	api['v1'] = issue['v1']
	api['v2'] = issue['v2']

	return api