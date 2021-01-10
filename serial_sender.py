import serial
from flask import request
from flask_api import FlaskAPI, status


app = FlaskAPI(__name__)
ready = "ready"
port_name = "/dev/cu.usbmodem143201"


def send_str_to_arduino(msg):
    with serial.Serial(port_name, 9600) as ser:
        print("Waiting for arduino...")
        ch = ser.read(len(ready))
        print("Arduino: " + ch.decode())
        msg = msg.ljust(32)
        msg = msg[:32] + "\n"
        print("Message: <", msg.encode(), ">")
        ser.write(msg.encode())
        return msg


@app.route("/api/version")
def version():
    return {"name": "send text to serial", "verison": "0.1"}


@app.route("/api/sendser", methods=["Post"])
def send_ser():
    msg = request.data.get("msg", "")
    if not msg:
        return "", status.HTTP_204_NO_CONTENT
    print(msg)
    sent = send_str_to_arduino(msg)
    return {"sent": sent}, status.HTTP_201_CREATED


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, debug=True)
