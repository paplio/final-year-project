from flask import Flask, render_template, request
from flask_restful import Resource, Api
import subtitle_ing
import os
from flask import send_file

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'irene'}

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

@app.route("/fromVideoExtractAudio", 
methods=['GET', 'POST'])
def uploadFromVideoExtractAudio():
        if request.method == 'POST':

                #getting the image from phone
                file = request.files['uploadedVideo']
                filename = file.filename
                tempdir = os.path.join("static/", filename)
                file.save(os.path.join("static/", filename))
                os.system("ffmpeg -i " + tempdir + " static/" + filename + ".mp3")
                return downloadExtractedAudio(filename)
        else:
                return "video-audio-extract endpoint"

@app.route("/downloadExtractedAudio", methods = ['GET', 'POST'])
def downloadExtractedAudio(path_to_audio_file):
        try:
                return send_file(os.path.join("static/", path_to_audio_file+".mp3"), as_attachment=True)
                #return send_file(os.path.join("static/", path_to_audio_file), attachment_filename=path_to_audio_file+".mp3", as_attachment=True)
        except Exception as e:
                return str(e)

@app.route("/compressVideo", methods = ['GET', 'POST'])
def compressVideo():
    if request.method == 'POST':
        file = request.files['uploadedVideo']
        filename = file.filename
        tempdir = os.path.join("static/", filename)
        file.save(os.path.join("static/", filename))
        os.system("ffmpeg -i " + tempdir + " -profile:v baseline -level 3.0 compressed_video.mp4")
        print(filename)
        return downloadCompressedVideo(filename)
    else:
        return "compressing-video-endpoint"

@app.route("/downloadCompressedVideo", methods = ['GET', 'POST'])
def downloadCompressedVideo(video_path):
        try:
                #return send_file(os.path.join("static/", video_path), as_attachment=True)
                return send_file(os.path.join("static/", "compressed_video.mp4"), as_attachment=True)
                #return send_file(os.path.join("static/", path_to_audio_file), attachment_filename=path_to_audio_file+".mp3", as_attachment=True)
        except Exception as e:
                return str(e)

if __name__ == '__main__':
        app.run(host = "0.0.0.0", port=8080)
