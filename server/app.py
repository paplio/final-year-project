from flask import Flask
from flask_restful import Resource, Api

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

if __name__ == '__main__':
    app.run(port=8000)