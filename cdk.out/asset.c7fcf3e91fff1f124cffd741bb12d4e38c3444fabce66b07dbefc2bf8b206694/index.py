import boto3
import os
from helpers import extract_zip, make_twilio_response
from urllib.parse import parse_qs

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['TABLE'])  # type:ignore


def handler(event, context):
    posted_body = event.get('body')
    twilio_data = parse_qs(posted_body)

    incoming_phone = twilio_data.get('From')[0]
    zipcode = twilio_data.get('Body')[0]
    zipcode = extract_zip(zipcode)
    print(zipcode, incoming_phone)
    if zipcode:
        table.update_item(
            Key={'phone_number': incoming_phone},
            UpdateExpression='set zip=:zip, active=:active',
            ExpressionAttributeValues={':zip': zipcode, ':active': True}
        )
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': make_twilio_response(f'Recieved {zipcode} from phone: {incoming_phone}')
    }
