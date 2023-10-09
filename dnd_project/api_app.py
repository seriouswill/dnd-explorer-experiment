import requests
from dnd_generator import execute_loop


url = "https://4bw6mh4tx2.execute-api.eu-west-2.amazonaws.com/v1/test"

response = requests.post(url, json=execute_loop(1))

if response.status_code == 200:
    print('Data received successfully!')
    print(response.text)
else:
    print('Failed to receive data!', response.status_code, response.text)
