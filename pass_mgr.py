#!/usr/bin/python3
""" Password Manager """

from os import urandom
from string import ascii_letters
from string import digits
import random
import sys

from hash_data import hash_information

from aws_parameters import delete_aws_parameter
from aws_parameters import write_aws_parameter
from aws_parameters import get_aws_parameter

ALT_CHARS = '@#$%^&*()'

def usage(function_name):
    """ print usage """
    print("Usage: %s <length> <account>" % function_name)

def generate_password(count, account):
    """ Generates a random password and ensures neither user nor account
        are in the Password
    """
    length = count
    chars = ascii_letters + digits + ALT_CHARS
    random.seed = (urandom(1024))

    # ensure account never appears in Password
    gen_pass = account
    while account in gen_pass:
        gen_pass = "".join(random.choice(chars) for i in range(length))

    return gen_pass


def store_password(account_name, store_value):
    """ Store posted password """
    write_aws_parameter(hash_information(account_name), store_value)

def create_password(account_name, pass_length):
    """ Create and store password of length pass_length """
    return generate_password(count=pass_length, account=account_name)

def retrieve_password(account_name):
    """ Retreive stored password """
    return get_aws_parameter(hash_information(account_name))

def update_password(account_name, pass_length):
    """ delete / create / store password """
    delete_password(account_name)
    pass_value = create_password(account_name, pass_length)
    store_password(account_name, pass_value)

def delete_password(account_name):
    """ delete password """
    delete_aws_parameter(hash_information(account_name))

def controller(method, account_name, pass_length, store_value):
    """ controller:  Decide what do """
    print("%s" % method)
    result = None
    if method:
        if method == 'S':
            store_password(account_name=account_name,
                           store_value=store_value)
        elif method == 'C':
            store_value = create_password(account_name=account_name,
                                          pass_length=pass_length)
            store_password(account_name=account_name,
                           store_value=store_value)
        elif method == 'R':
            result = retrieve_password(account_name=account_name)
        elif method == 'U':
            update_password(account_name=account_name,
                            pass_length=pass_length)
        elif method == 'D':
            delete_password(account_name=account_name)
        else:
            usage(sys.argv[0])

    return result
