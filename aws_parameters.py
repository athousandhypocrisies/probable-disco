""" AWS Parameter Implementation """

import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import ProfileNotFound

def ensure_profile(m_profile_name, default_value):
    """ Ensure value """
    if not m_profile_name:
        m_profile_name = default_value
    return m_profile_name

def get_ssm_client(m_profile_name, m_region_name):
    """ Shared code to get ssm client """
    ssm = None
    try:
        session = boto3.Session(
            profile_name=ensure_profile(m_profile_name, 'default'))
        ssm = session.client(
            service_name='ssm',
            region_name=ensure_profile(m_region_name, 'us-east-1'))
    except ProfileNotFound:
        print("profile name not found, trying boto3.client('ssm').")

    if not ssm:
        ssm = boto3.client('ssm')

    return ssm
def key_dne():
    """ Default error message for key dne """
    print("Error: key does not exist")

def delete_aws_parameter(m_key, m_profile_name=None, m_region_name=None):
    """ remove key/value pair from aws parameter store """
    ssm = get_ssm_client(m_profile_name, m_region_name)
    try:
        ssm.delete_parameter(Name=m_key)
    except ClientError:
        key_dne()

def get_aws_parameter(m_key, m_profile_name=None, m_region_name=None):
    """ Retrieve parameter value """
    ret_val = None
    ssm = get_ssm_client(m_profile_name, m_region_name)
    try:
        ssm_detail = ssm.get_parameter(Name=m_key,
                                       WithDecryption=True)
        if ssm_detail:
            parameter_detail = ssm_detail['Parameter']
            if parameter_detail:
                ret_val = parameter_detail['Value']
    except ClientError:
        key_dne()

    return ret_val

def write_aws_parameter(m_key,
                        m_value,
                        m_profile_name=None,
                        m_region_name=None):
    """ Write the kvp to the parameter store """
    print("AWS: write_aws_parameter")
    ssm = get_ssm_client(m_profile_name, m_region_name)
    try:
        ssm.put_parameter(Name=m_key,
                          Value=m_value,
                          Type='SecureString',
                          Overwrite=True)
    except ClientError:
        print("Error: write failure")
