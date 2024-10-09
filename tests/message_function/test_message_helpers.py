import pytest
from datetime import datetime
from freezegun import freeze_time
from urllib.parse import urlparse
from urllib.parse import parse_qs

import lambda_functions.message_function.helpers as helpers


@pytest.mark.parametrize(
    "start_hour,expected",
    [
        (0, 0),
        (12, 12),
        (23, 23)
    ])
def test_start_hour_url(start_hour, expected):
    url = helpers.get_weather_url(start_hour, 3, ['99577', '99576'])
    parsed = urlparse(url)
    start_params = parse_qs(parsed.query)['begin']
    assert len(start_params) == 1
    assert datetime.fromisoformat(start_params[0]).hour == expected


@pytest.mark.parametrize(
    'start_date,expected',
    [
        ("2024-01-14", "2024-01-15T"),
        ("2024-12-31", "2025-01-01T"),
        ("2020-02-28", "2020-02-29T"),
        ("2021-02-28", "2021-03-01T"),
    ]
)
def test_url_date(start_date, expected):
    with freeze_time(start_date):
        url = helpers.get_weather_url(0, 3, ['99577', '99576'])
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        assert params['begin'][0].startswith(expected)
        assert params['end'][0].startswith(expected)


@pytest.mark.parametrize(
    'zip_list,expected',
    [
        (['99577', '99576'], "99577 99576"),
        (['99577'], "99577")
    ]
)
def test_url_zips(zip_list, expected):
    url = helpers.get_weather_url(0, 3, zip_list)
    parsed = urlparse(url)
    zip_params = parse_qs(parsed.query)['zipCodeList']
    assert len(zip_params) == 1
    assert zip_params[0] == expected


def test_weather_data_parse(weather_xml):
    '''It should find the minimum temp'''
    zip_dict = helpers.parse_weather_data(weather_xml)
    assert zip_dict[helpers.local_zips[0]] == 31
    assert zip_dict[helpers.local_zips[1]] == 29


def test_weather_data_null(weather_xml):
    '''If the API returns null values for temps is should set that zip to None'''
    zip_dict = helpers.parse_weather_data(weather_xml)
    assert zip_dict[helpers.local_zips[2]] is None
