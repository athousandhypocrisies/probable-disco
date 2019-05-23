""" Hashing functions """

from hashlib import sha224

def hash_string_deep(string_value, hash_count):
    """ better hash (recursive) for account name for security """
    l_string = hash_information(string_value)
    if hash_count > 1:
        l_string = hash_string_deep(l_string, hash_count -1)
    return l_string

def hash_string(string_value):
    """ Hash 224 the input value """
    return hash_string_deep(string_value, 10)

def hash_information(information_value):
    """ Hash 224 the input value """
    if not information_value:
        information_value = ""
    return sha224(bytes(information_value, encoding='utf-8')).hexdigest()
