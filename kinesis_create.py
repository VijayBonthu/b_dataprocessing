
import boto3
from botocore.exceptions import ClientError
from customlogging import setup_logger

class AwsServices:
    def __init__(self,services:list):
        for service in services:
            try:
                f"{service}_client" = boto3.client(service)
                print(f"Initializing service: {service}")
                setup_logger(f"{service}_client")
                
            except Exception as e:
                print(f"{service} failed error: e")
                setup_logger(f"{service}_client")

    def create_kinesis(self,stream_name:str, stream_mode:str = "ON_DEMAND"):

        # Create a Kinesis client
        kinesis_client = boto3.client('kinesis')

        # Create the Kinesis stream
        try:
            response = kinesis_client.describe_stream(StreamName = stream_name)
            setup_logger(response)

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
        

