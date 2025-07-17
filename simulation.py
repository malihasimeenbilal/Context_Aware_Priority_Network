import requests
import time
import random

sources = ['ambulance', 'hospital', 'user', 'fire-dept']
types = ['emergency', 'normal']

while True:
    payload = {
        'source': random.choice(sources),
        'type': random.choice(types),
        'required_bandwidth': random.randint(5, 30),
        'duration': random.randint(10, 30)
    }
    res = requests.post('http://127.0.0.1:5000/request', json=payload)
    print(payload, '->', res.json())
    time.sleep(2)
