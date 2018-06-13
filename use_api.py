import requests
import json
import random
import os


def creat_user(users):
    url = "http://a8843526.ddns.net/api/auth/sign"
    headers = {
        'content-type': "application/json"
    }
    session = []
    for u in users:
        payload = json.dumps(u)
        response = requests.request("POST", url, data=payload, headers=headers)
        res = json.loads(response.text)
        if res["status"] in [201, 200]:
            u["session"] = response.cookies["session"]
            session += [u]

    return session


def post_image(users):
    url = "http://a8843526.ddns.net/api/image/post"
    path = os.getcwd()
    headers = {
        'content-type': "application/json"
    }
    with os.scandir(f"{path}/images") as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                file_name = entry.name
                with open(f"{path}/images/{file_name}", mode="rb") as im:
                    ran_id = random.randrange(10)
                    b64 = im.readline().decode("utf-8")
                    users[ran_id]["payload"] += [b64]

    for u in users:
        cookies = dict(session=u['session'])
        response = requests.request("PUT", url, data=json.dumps(u['payload']), headers=headers, cookies=cookies)
        print(response.text)


if __name__ == '__main__':
    users_data = [{"username": "test0001", "password": "11111111", "payload": []},
                  {"username": "test0002", "password": "11111111", "payload": []},
                  {"username": "test0003", "password": "11111111", "payload": []},
                  {"username": "test0004", "password": "11111111", "payload": []},
                  {"username": "test0005", "password": "11111111", "payload": []},
                  {"username": "test0006", "password": "11111111", "payload": []},
                  {"username": "test0007", "password": "11111111", "payload": []},
                  {"username": "test0008", "password": "11111111", "payload": []},
                  {"username": "test0009", "password": "11111111", "payload": []},
                  {"username": "test0010", "password": "11111111", "payload": []}]

    users_data = creat_user(users_data)
    post_image(users_data)
