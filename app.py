import requests
from dnd_generator import execute_loop
import os
from dotenv import load_dotenv
import boto3
import json

load_dotenv()


aws_access_key_id = os.getenv('AWS_ACCESS_KEY_MONSTER')
aws_secret_access_key = os.getenv('AWS_SECRET_KEY_MONSTER')

# Define the API endpoint URL
api_url = "https://4bw6mh4tx2.execute-api.eu-west-2.amazonaws.com/v1/test"

count = 0
while count < 1:
    count += 1
    if aws_access_key_id is None or aws_secret_access_key is None:
        raise ValueError("AWS credentials not found in .env file")

    # Define the data you want to send (if any)
    payload = {"data":execute_loop(1)}

    aws_region = 'eu-west-2'
    client = boto3.client('lambda', 
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=aws_region)

    lambda_function_name = 'arn:aws:lambda:eu-west-2:404544469985:function:monster_handler'


    # Invoke the Lambda function
    response = client.invoke(
        FunctionName=lambda_function_name,
        InvocationType='RequestResponse',  # Use 'RequestResponse' for synchronous execution
        Payload=json.dumps(payload)  # Serialize the payload to JSON
    )

    # Process the Lambda function's response
    if response['StatusCode'] == 200:
        result = json.loads(response['Payload'].read().decode())
        print("Lambda Function Response:", result)
    else:
        print("Lambda Function Invocation Failed")



