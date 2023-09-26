import requests
from dnd_generator import execute_loop


# Define the API endpoint URL
api_url = "https://eqshii7ong.execute-api.eu-west-2.amazonaws.com"

# Set up any necessary headers or request parameters
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"  # Add authorization headers if required
}

# Define the data you want to send (if any)
payload = {
    execute_loop(5)
}

# Make the HTTP request
try:
    response = requests.post(api_url, headers=headers, json=payload)

    # Check the response status code and handle accordingly
    if response.status_code == 200:
        print("Request was successful!")
        print("Response:", response.text)
    else:
        print("Request failed with status code:", response.status_code)
        print("Response:", response.text)

except Exception as e:
    print("An error occurred:", str(e))



