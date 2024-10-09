from constructs import Construct

from aws_cdk import (
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_
)


class PluginService(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        table = dynamodb.Table(
            self,
            'plugin_users',
            partition_key={
                "name": 'phone_number',
                "type": dynamodb.AttributeType.STRING
            }
        )

        messenger = lambda_.Function(
            self, "MessageHandler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset(
                'lambda_functions/',
                exclude=['subscriber_function/*', 'conftest.py'],
             ),
            handler='message_function.index.handler',
            environment=dict(
                TABLE=table.table_name
                )
        )

        handler = lambda_.Function(
            self, "SubscribeHandler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset(
                'lambda_functions/',
                exclude=['message_function/*', 'conftest.py'],
            ),
            handler='subscriber_function.index.handler',
            environment=dict(
                TABLE=table.table_name
                )
        )

        api = apigateway.RestApi(self, "sms-api",
                                 rest_api_name="Plugin at 20 Service",
                                 description="This service handles plugin requests")

        resource = api.root.add_resource("subscribe")
        lambda_int = apigateway.LambdaIntegration(handler)  # type:ignore

        resource.add_method("POST", lambda_int)
        resource.add_method("GET", lambda_int)
        resource.add_method("DELETE", lambda_int)

        table.grant_read_write_data(handler)
        table.grant_read_write_data(messenger)
