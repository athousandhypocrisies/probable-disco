""" Lambda hander for password manager """

from pass_mgr import controller

def lambda_handler(event, context):
    """ default lambda_handler """
    inputs = event
    if inputs.get('queryStringParameters'):
        inputs = inputs.get('queryStringParameters')

    method = str.upper(inputs.get('method'))
    account_name = str.upper(inputs.get('account_name'))
    pass_length = int(inputs.get('length', 10))
    store_value = str(inputs.get('store_value', None))

    result = controller(method, account_name, pass_length, store_value)

    if not result:
        result = 'Hello from Lambda!'
    print("%s:version:[%s]" % (context.function_version, context.function_name))
    return {
        'statusCode': 200,
        'body': result
    }
