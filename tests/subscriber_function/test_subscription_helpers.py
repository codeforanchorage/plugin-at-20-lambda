import pytest
import lambda_functions.subscriber_function.helpers as helpers


@pytest.mark.parametrize(
    "zipcode,expected",
    [
        ('99577', '99577'),
        ('99503-1234', '99503'),
        ('99501 9098', '99501')
    ])
def test_extract_good_zip(zipcode, expected):
    '''Should return the five digit zipcode'''
    extracted = helpers.extract_zip(zipcode)

    assert expected == extracted


def test_extract_non_local_zip():
    '''Non-local zip codes should raise NotLocalZipError'''
    with pytest.raises(helpers.NotLocalZipError):
        helpers.extract_zip('77102')


@pytest.mark.parametrize("zipcode", ['1', 'hello', '', '99577656', None])
def test_extract_bad_zip(zipcode):
    '''Input that doesn't look like a zip should return none'''
    with pytest.raises(ValueError):
        helpers.extract_zip(zipcode)
