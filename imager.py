import os
import base64
import subprocess
from flask import request
from flask_api import FlaskAPI, status


app = FlaskAPI(__name__)
ffmpeg_cmd = 'ffmpeg -f avfoundation -framerate 30 -video_size 1280X720 -i "1:none" -vframes 1 out.jpg -y'
base64_img = None

def enabled():
    with open('imager.cfg', 'r') as imager_cfg:
        text = imager_cfg.read()
        return text.strip() == '1'

def call_ffmpeg():
    global base64_img
    process = subprocess.Popen(ffmpeg_cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    with open("out.jpg", "rb") as image_file:
        base64_img = base64.b64encode(image_file.read())
        os.remove('out.jpg')
        base64_img = base64_img.decode('utf-8')
    return process.returncode

@app.route("/api/enabled", methods=["GET"])
def pic_enabled():
    return {"enabled": enabled()}

@app.route("/api/takePic", methods=["GET"])
def take_pic():
    global base64_img
    if not enabled():
        return {}, 403
    try:
        retval = call_ffmpeg()
        return {"process": retval}, 200
    except:
        return {}, 500

@app.route("/api/hasPic", methods=["GET"])
def has_pic():
    has_pic = bool(base64_img)
    return {"hasPic": has_pic}, 200

@app.route("/api/getPic", methods=["GET"])
def get_pic():
    global base64_img
    try:
        return {"picture": base64_img}, 200
    finally:
        base64_img = None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9002, debug=True)
