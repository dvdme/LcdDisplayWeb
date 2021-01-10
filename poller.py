import requests
import time

#api_url_has = "http://127.0.0.1:82/api/hasMessage"
#api_url_get = "http://127.0.0.1:82/api/getMessage"
#api_url_clear_img = "http://127.0.0.1:82/api/clearImage"
#api_url_post_img = "http://127.0.0.1:82/api/postImage"
api_url_has = "http://msg.dme.ninja/api/hasMessage"
api_url_get = "http://msg.dme.ninja/api/getMessage"
api_url_clear_img = "http://msg.dme.ninja/api/clearImage"
api_url_post_img = "http://msg.dme.ninja/api/postImage"
api_url_send = "http://127.0.0.1:9001/api/sendser"
api_url_imager = "http://127.0.0.1:9002/api/"


def eval_image():
    req = requests.get(f"{api_url_imager}enabled", timeout=10)
    rsp = req.json()
    print(rsp)
    if not rsp["enabled"]:
        req = requests.get(api_url_clear_img, timeout=10)
        print(req.json())


def send_image():
    req = requests.get(f"{api_url_imager}takePic", timeout=10)
    print(req.json())
    req = requests.get(f"{api_url_imager}hasPic", timeout=10)
    print(req.json())
    if req.json()["hasPic"]:
        req = requests.get(f"{api_url_imager}getPic", timeout=10)
        pic = req.json()["picture"]
        req = requests.post(api_url_post_img, data={"img": pic}, timeout=10)
        print(req.json())


def main_poll():
    rsp = requests.get(api_url_has, timeout=10).json()
    print(rsp)
    if rsp["hasMessage"]:
        print("Has message")
        rsp = requests.get(api_url_get, timeout=10).json()
        print(rsp)
        msg = rsp["message"]
        req = requests.post(api_url_send, data={"msg": msg}, timeout=10)
        print(req.status_code, req.reason)
        return True
    return False


def pool():
    while True:
        try:
            eval_image()
            if main_poll():
                send_image()
        except Exception as ex:
            print(ex)
        finally:
            time.sleep(10)


if __name__ == "__main__":
    pool()
