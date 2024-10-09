# flake8: noqa 501

import re

from common.zipcodes import local_zips

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


messages = {
    "WELCOME": "Hello there from Code for Anchorage & Anchorage DHHS, just send me your zipcode and I'll send you an evening reminder to plug in your car if it'll be below 20 degrees at night.",
    "GOODBYE": "You've been unsubscribed. Later!",
    "BAD_ZIP": "Your zip code isn't in Anchorage and the thing is that we only know about the weather in Anchorage. Sorry, we can't help you.",
    "CONFIRMATION": "Alrighty, you're signed up. Send STOP if you want the messages to stop and START if you change your mind after stopping.",
    "INSTRUCTIONS": "Sorry, I don't know what you want. Send STOP if you want the messages to stop and START if you change your mind after stopping.",
}
