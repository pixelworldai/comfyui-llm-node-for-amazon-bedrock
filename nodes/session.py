import requests
from retry import retry
import boto3
import configparser
from pathlib import Path

MAX_RETRY = 3


def load_aws_config():
    """Load AWS credentials from config.ini file if it exists."""
    config_path = Path(__file__).parent.parent / "config.ini"
    if not config_path.exists():
        return None
    config = configparser.ConfigParser()
    config.read(config_path)
    if 'aws' not in config:
        return None
    aws_section = config['aws']
    required_keys = ['access_key_id', 'secret_access_key']
    if not all(k in aws_section for k in required_keys):
        return None
    credentials = {
        'aws_access_key_id': aws_section['access_key_id'],
        'aws_secret_access_key': aws_section['secret_access_key'],
    }
    if 'region' in aws_section:
        credentials['region_name'] = aws_section['region']
    return credentials


@retry(tries=MAX_RETRY)
def get_client(service_name, clients={}):
    if service_name in clients:
        return clients[service_name]

    aws_credentials = load_aws_config()
    try:
        if aws_credentials:
            clients[service_name] = boto3.client(service_name=service_name, **aws_credentials)
            print(f"Using AWS credentials from config.ini for {service_name}")
        else:
            clients[service_name] = boto3.client(service_name=service_name)
            print(f"Using default AWS credential chain for {service_name}")
    except Exception as e:
        # get region from gateway
        response = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={
                "X-aws-ec2-metadata-token-ttl-seconds": "21600",
            },
        )
        token = response.text
        response = requests.get(
            "http://169.254.169.254/latest/meta-data/placement/region",
            headers={
                "X-aws-ec2-metadata-token": token,
            },
        )
        boto3.setup_default_session(region_name=response.text)
        print("Automatically set region to", response.text)
        clients[service_name] = boto3.client(service_name=service_name)
    return clients[service_name]
