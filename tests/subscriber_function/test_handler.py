import os
from unittest import mock
from botocore.stub import Stubber
from lambda_functions.subscriber_function.helpers import messages

from lambda_functions.subscriber_function.index import handler, ddb


@mock.patch.dict(os.environ, {"TABLE": "TEST_TABLE"})
class TestHandler:

    def test_handler_good_input(self):
        '''
        It should update dynampodb table and respond with a confirmation
        given a local zipcode
        '''
        phone = '+1907555121'
        zip = '99577'
        body = {'body': f"From={phone}&Body={zip}"}

        expected_DDB_params = {
            'ExpressionAttributeValues': {':active': True, ':zip': '99577'},
            'Key': {'phone_number': ' 1907555121'},
            'TableName': 'TEST_TABLE',
            'UpdateExpression': 'set zip=:zip, active=:active'
        }

        with Stubber(ddb.meta.client) as stub:
            stub.add_response('update_item', {}, expected_DDB_params)
            res = handler(body, None)

        assert res['statusCode'] == 200
        assert res['body'] == messages['CONFIRMATION']

    def test_handler_non_local_zip(self):
        '''
        It should respond with a badzip response and not
        update dynamodb given and non-local zip
        '''
        phone = '+1907555121'
        zip = '77502'
        body = {'body': f"From={phone}&Body={zip}"}

        with Stubber(ddb.meta.client) as stub:
            res = handler(body, None)
            stub.assert_no_pending_responses()

        assert res['statusCode'] == 200
        assert res['body'] == messages['BAD_ZIP']

    def test_handler_bad_input(self):
        '''
        It should respond with instructions and not update
        dynamodb given input that is not a zipcode
        '''

        phone = '+1907555121'
        zip = 'ab 77502'
        body = {'body': f"From={phone}&Body={zip}"}

        with Stubber(ddb.meta.client) as stub:
            res = handler(body, None)
            stub.assert_no_pending_responses()

        assert res['statusCode'] == 200
        assert res['body'] == messages['INSTRUCTIONS']
