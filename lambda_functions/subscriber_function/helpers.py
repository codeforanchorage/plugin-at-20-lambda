# flake8: noqa 501

import re

zip_rx = re.compile(r'^(\d{5})(?:[-\s]\d{4})?$')


class NotLocalZipError(Exception):
    pass


def extract_zip(zip_string):
    '''
    Returns the five digit zip if the string looks
    like a zip code otherwise None
    '''
    try:
        match = zip_rx.match(zip_string)
    except TypeError:
        raise ValueError("Not a Zipcode")

    if match is None:
        raise ValueError("Not a Zipcode")

    five_digit_zip = match.group(1)
    if five_digit_zip not in local_zips:
        raise NotLocalZipError

    return five_digit_zip


local_zips = set([
    # anchorage
    '99501',
    '99502',
    '99503',
    '99504',
    '99507',
    '99508',
    '99509',
    '99510',
    '99511',
    '99513',
    '99514',
    '99515',
    '99516',
    '99517',
    '99518',
    '99519',
    '99520',
    '99521',
    '99522',
    '99523',
    '99524',
    '99599',
    '99577',
    '99695',

    # matsu
    '99652',
    '99694',
    '99645',
    '99667',
    '99674',
    '99676',
    '99683',
    # '99629', # causes a weather service error
    '99654',
    '99687',
    '99688'
    ])

messages = {
    "WELCOME": "Hello there from Code for Anchorage & Anchorage DHHS, just send me your zipcode and I'll send you an evening reminder to plug in your car if it'll be below 20 degrees at night.",
    "GOODBYE": "You've been unsubscribed. Later!",
    "BAD_ZIP": "Your zip code isn't in Anchorage and the thing is that we only know about the weather in Anchorage. Sorry, we can't help you.",
    "CONFIRMATION": "Alrighty, you're signed up. Send STOP if you want the messages to stop and START if you change your mind after stopping.",
    "INSTRUCTIONS": "Sorry, I don't know what you want. Send STOP if you want the messages to stop and START if you change your mind after stopping.",
}
