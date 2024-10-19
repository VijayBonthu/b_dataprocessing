
import boto3
from botocore.exceptions import ClientError

def create_kinesis(stream_name:str, stream_mode:str = "ON_DEMAND"):

    # Create a Kinesis client
    kinesis_client = boto3.client('kinesis')

    # Create the Kinesis stream
    try:
        response = kinesis_client.describe_stream(StreamName = stream_name)

        return f"Kinesis stream {stream_name} already exist Stream status: {response['StreamDescription']['StreamStatus']}"
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            response = kinesis_client.create_stream(
            StreamName=stream_name,
            StreamModeDetails={
                'StreamMode': stream_mode
            }
            )
            return response
        else:
            return f"error occured {e.response['Error']}"
        


    # Print the response to confirm the update
    # print(response)