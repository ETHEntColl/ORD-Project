import glob
from flask import Flask, render_template, url_for
import os

static_folder = 'Z:/01_SCANNED_AND_PROCESSED/02 FINAL/'

app = Flask(__name__, static_folder=static_folder)
project_path = static_folder
projects = projects = glob.glob(project_path+"*\\")
project_names = [project.split("\\")[-2] for project in projects]
curr = -1

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/getNext")
def getNext():
    global curr
    if curr < len(projects) - 1:
        curr += 1
        return render_template('viewer.html', path=url_for('static', filename=project_names[curr] + '/' + 'Model/' + project_names[curr] +'.glb'), name=project_names[curr])
    else:
        return "Finished!"

if __name__ == "__main__":
    app.run()
