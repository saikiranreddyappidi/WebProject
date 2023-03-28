import requests
text=requests.get("http://192.168.96.118:8000/project/testing")
print(text.text)
print(text,type(text))