from flask import Flask, make_response, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/maven-reaction"
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
		'bc': form['bc'],
		'detectionId': form['detectionId'],
		'useId': form['useId'],
		'path': form['path']
	}
	issues.insert_one(issue)
	response = make_response()
	response.status_code = 201
	return response

def show_issues():
	return render_template('issues.html')
