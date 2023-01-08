import json
import requests
headers = {"Authorization": "Bearer ya29.a0Aa4xrXM8IaHeA6pslX0xr92LdRXY88DMXh6A912qhxD6bAt9-rkXeL8waxSQnCyM_z8ONa4LNxGHHACszrNwQH8fzDXVq2OtD6ELxL2f7y2gn6iAiWayQ_1tZkflLzRucdkjNjhR3NvcbnjN4s5b27kD_qBzaCgYKATASARASFQEjDvL9ljmKpWvHXa5fJS9h-T5_cQ0163"}
para = {
    "name": "searching.jpg",
    "parents": ['1DpZEC-2cTjZIHh5wbzAr7AURLaAL8rEY'],
}
files = {
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    'file': open("./search.jpg", "rb")
}
r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers=headers,
    files=files
)
print(r.text)
