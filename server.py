import time
from flask import Flask, request, render_template, jsonify


app = Flask(__name__)
last_message = None
last_message_time = 0
offline_time = 30
image = None


def lcd_status():
    value = abs(last_message_time - int(time.time()))
    #print(value)
    if value > 30:
        return "offline"
    else:
        return "online"


@app.route("/robots.txt", methods=["GET"])
def robots():
    return """
User-agent: *
Disallow: /
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global last_message
    global image
    if request.method == "POST":
        last_message = request.form["msg"]
        print("Got message: ", last_message)
    if image and not image.startswith('data'):
        image = 'data:image/png;base64,' + image
    return render_template("index.html", lcd_status=lcd_status(), has_image=False, image=image)

@app.route("/api/getImage", methods=["GET"])
def get_image():
    global image
    if image:
        image = image.replace('data:image/png;base64,', '')
        return jsonify({'image': image}), 200
    else:
        return {}, 404

@app.route("/api/hasMessage")
def has_message():
    global last_message_time
    last_message_time = int(time.time())
    rsp = {"hasMessage": bool(last_message)}
    print(rsp)
    return jsonify(rsp)


@app.route("/api/getMessage")
def get_message():
    global last_message
    rsp = {"message": last_message}
    last_message = None
    print(rsp)
    return jsonify(rsp)

@app.route("/api/postImage", methods=["POST"])
def post_image():
    global image
    image = request.form.get("img", "")
    return jsonify({"image": len(image)})

@app.route("/api/clearImage", methods=["GET"])
def clear_image():
    global image
    image = None
    return jsonify({"image": image})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=82, debug=True)
