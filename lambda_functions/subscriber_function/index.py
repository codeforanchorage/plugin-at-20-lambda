import os
from urllib.parse import parse_qs
import boto3
from .helpers import extract_zip, messages, NotLocalZipError

ddb = boto3.resource('dynamodb')


def response(message, status_code=200):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': message
    }


def handler(event, context):
    table = ddb.Table(os.environ['TABLE'])  # type:ignore

    posted_body = event.get('body')
    twilio_data = parse_qs(posted_body)

    from_field = twilio_data.get('From')
    body = twilio_data.get('Body')

    if from_field is None or body is None:
        return response('bad input', 422)

    incoming_phone = from_field[0]

    try:
        zipcode = extract_zip(body[0])
    except ValueError:
        return response(messages['INSTRUCTIONS'])
    except NotLocalZipError:
        return response(messages['BAD_ZIP'])

    print(zipcode, incoming_phone)

    if zipcode:
        table.update_item(
            Key={'phone_number': incoming_phone},
            UpdateExpression='set zip=:zip, active=:active',
            ExpressionAttributeValues={':zip': zipcode, ':active': True}
        )

    return response(messages['CONFIRMATION'])
