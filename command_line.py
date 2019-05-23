""" Command line use of password manager """

import sys
from argparse import ArgumentParser
from pass_mgr import controller
from pass_mgr import usage

def validate_input():
    """ Validate the input data to the program call """
    pass_length = None
    account_name = None
    method = None
    in_value = None
    parser = ArgumentParser()
    parser.add_argument("-l", "--length",
                        type=int,
                        help="length of password")

    parser.add_argument("-a", "--account",
                        help="account or site name")

    parser.add_argument("-m", "--method",
                        help="method to take [S|C|R|U|D]")

    parser.add_argument("-v", "--value",
                        help="Do not generate, store this value")

    args = parser.parse_args()
    if args.length:
        pass_length = int(args.length)

    if args.account:
        account_name = str(args.account)

    if args.method:
        method = str.upper(args.method)

    if args.value:
        in_value = str(args.value)

    return (pass_length, account_name, method, in_value)

if __name__ == "__main__":
    G_PASS_LENGTH, G_ACCOUNT_NAME, G_METHOD, G_PASSWORD = validate_input()

    if G_METHOD:
        controller(method=G_METHOD,
                   account_name=G_ACCOUNT_NAME,
                   pass_length=G_PASS_LENGTH,
                   store_value=G_PASSWORD)
    else:
        usage(sys.argv[0])
