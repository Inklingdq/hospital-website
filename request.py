import requests

url = 'http://localhost:5000/results'
r = requests.post(url,json={'file':'hhk'})

print(r.json())
