import json
import base64


def encode(msg):
    for i in msg:
        msg[i] = str(base64.urlsafe_b64encode(msg[i].encode("utf-8")), "utf-8")
    return json.dumps(msg)


def decode(msg):
    msg = json.loads(msg)
    for i in msg:
        msg[i] = base64.urlsafe_b64decode(msg[i]).decode('utf8')
    return msg
