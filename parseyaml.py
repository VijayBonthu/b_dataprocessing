import yaml
import subprocess
import os
from dotenv import load_dotenv

load_dotenv(override=True)
with open("services.yaml", "r") as file:
    config = yaml.safe_load(file)

#allowed services
allowed_platforms = ["AWS", "GOOGLE","MICROSOFT AZURE"]

environment  = config["cloud services"]["platforms"]
   
def resolve_value(value):
    if isinstance(value, str) and value.startswith("$"):
        env_var = value[2:-1]
        return os.getenv(env_var)
    return value

#subprocesses to run the clod specific login authetication
def configure_aws(userid, password, region, output):
    print(f"Configuration AWS with the userid: {userid}")
    try:
        subprocess.run(['aws', 'configure', 'set', 'aws_access_key_id', userid])
        subprocess.run(['aws','configure', 'set', 'aws_secret_access_key', password])
        subprocess.run(['aws','configure', 'set', 'region', region])
        subprocess.run(['aws', 'configure', 'set', 'output', output])
        print("Accepted the details AWS is ready with configured details")
    except Exception as e:
        print(f" error occur {e} make use you provide correct credentials and region and output of your data like Json, csv")

configure_aws(userid= resolve_value(config['cloud services']['config']['AWS']['user_id']),
              password= resolve_value(config['cloud services']['config']['AWS']['password']),
              region= resolve_value(config['cloud services']['config']['AWS']['Default region name']),
              output=resolve_value(config['cloud services']['config']['AWS']['Default output format'])
              )

def configure_google(userid, password, region, output):
    print(f"Configuration AWS with the userid: {userid}")
    try:
        subprocess.run(['aws', 'configure', 'set', 'aws_access_key_id', userid])
        subprocess.run(['aws','configure', 'set', 'aws_secret_access_key', password])
        subprocess.run(['aws','configure', 'set', 'region', region])
        subprocess.run(['aws', 'configure', 'set', 'output', output])
        print("Accepted the details AWS is ready with configured details")
    except Exception as e:
        print(f" error occur {e} make use you provide correct credentials and region and output of your data like Json, csv")

configure_aws(userid= resolve_value(config['cloud services']['config']['AWS']['user_id']),
              password= resolve_value(config['cloud services']['config']['AWS']['password']),
              region= resolve_value(config['cloud services']['config']['AWS']['Default region name']),
              output=resolve_value(config['cloud services']['config']['AWS']['Default output format'])
              )

def configure_azure(userid, password, region, output):
    print(f"Configuration AWS with the userid: {userid}")
    try:
        subprocess.run(['aws', 'configure', 'set', 'aws_access_key_id', userid])
        subprocess.run(['aws','configure', 'set', 'aws_secret_access_key', password])
        subprocess.run(['aws','configure', 'set', 'region', region])
        subprocess.run(['aws', 'configure', 'set', 'output', output])
        print("Accepted the details AWS is ready with configured details")
    except Exception as e:
        print(f" error occur {e} make use you provide correct credentials and region and output of your data like Json, csv")

# Google Cloud configuration function
def configure_google(project_id, service_account_key):
    try:
        subprocess.run(['gcloud', 'config', 'set', 'project', project_id])
        subprocess.run(['gcloud', 'auth', 'activate-service-account', '--key-file', service_account_key])
        print("Google Cloud configured successfully.")
    except Exception as e:
        print(f"Error during Google Cloud configuration: {e}")

for platform in environment:
    if platform.upper() not in allowed_platforms:
        raise ValueError(f"platform: '{platform}' is not supported, platforms can only be {allowed_platforms}")
    
    elif platform.upper() == "AWS":
        aws_config = config['cloud services']['config']['AWS']
        configure_aws(userid= resolve_value(aws_config['user_id']),
                password= resolve_value(aws_config['password']),
                region= resolve_value(aws_config['Default region name']),
                output=resolve_value(aws_config['Default output format'])
                )
    elif platform == 'GOOGLE':
            
            google_config = config['cloud services']['config']['GOOGLE']
            configure_google(
            project_id=resolve_value(google_config['project_id']),
            service_account_key=resolve_value(google_config['service_account_key'])
            )
    elif platform == 'MICROSOFT AZURE':
        azure_config = config['cloud services']['config']['MICROSOFT AZURE']
        configure_azure(
            app_id=resolve_value(azure_config['app_id']),
            password=resolve_value(azure_config['password']),
            tenant_id=resolve_value(azure_config['tenant_id'])
        )



