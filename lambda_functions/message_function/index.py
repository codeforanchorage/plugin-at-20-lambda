import os
import boto3
from boto3.dynamodb.conditions import (Attr)

from .helpers import get_weather_url, get_weather_data, parse_weather_data
from common.zipcodes import local_zips

ddb = boto3.resource('dynamodb')


LOW_TEMP_START_HOUR = 0
LOW_TEMP_END_HOUR = 3
NOTIFICATION_TEMPERATURE = 20


def response(message, status_code=200):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': message
    }


def get_users():
    table = ddb.Table(os.environ['TABLE'])  # type:ignore

    response = table.scan(
        FilterExpression=Attr('active').eq(True)
    )
    return response['Items']


def handler(event, context):
    url = get_weather_url(LOW_TEMP_START_HOUR, LOW_TEMP_END_HOUR, local_zips)
    data = get_weather_data(url)
    temps = parse_weather_data(data)

    users = get_users()
    to_send = [(user['phone_number'], temps[user['zip']]) for user in users]
    return response(to_send)
