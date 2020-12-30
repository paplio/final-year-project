from flask import Flask, render_template, request
from flask_restful import Resource, Api
import subtitle_ing
import os

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

@app.route("/")
def default():
	return "Testing client-server connectivity on localhost!"

@app.route("/upload")
def upload():
    return "This is the API endpoint we are trying to hit."

@app.route("/manualupload")
def manualupload():
	return render_template('manual.html')

@app.route("/converting", methods = ['GET', 'POST'])
def converting():
	if request.method == 'POST':
		f = request.files['myfile']
		f.save(os.path.join("static/",f.filename))
		subtitle_ing.convert(f.filename)
		pathThing = os.path.join("" + "subbed-"+f.filename)
		return showfile(pathThing)

@app.route("/viewfile")
def showfile(filename):
	return render_template('showfile.html', filename = filename)

if __name__ == '__main__':
	app.run(port=8000)