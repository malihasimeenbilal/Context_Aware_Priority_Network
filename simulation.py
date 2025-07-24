import requests
import time
import random

# Extended list of traffic/emergency sources
sources = [
    'ambulance',
    'hospital',
    'user',
    'fire-dept',
    'traffic-control',
    'police-department',
    'public-transport',
    'emergency-alert (911)'
]

# Types of messages
types = ['emergency', 'normal']

# Infinite simulation loop
while True:
    payload = {
        'source': random.choice(sources),
        'type': random.choice(types),
        'required_bandwidth': random.randint(5, 30),  # in Mbps maybe
        'duration': random.randint(10, 30)  # in seconds
    }
    
    try:
        res = requests.post('http://127.0.0.1:5000/request', json=payload)
        print(payload, '->', res.json())
    except Exception as e:
        print(payload, '-> ERROR:', e)
    
    time.sleep(2)
