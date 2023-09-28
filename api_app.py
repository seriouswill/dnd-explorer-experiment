import requests
import json
from dnd_generator import execute_loop

url = "https://qodlc1vxkk.execute-api.eu-west-2.amazonaws.com/monsters"

data = execute_loop(1)  # assuming this returns a dictionary

response = requests.post(url, json=data)

if response.status_code == 200:
    print('Data sent successfully!')
else:
    print('Failed to send data!', response.status_code, response.text)
