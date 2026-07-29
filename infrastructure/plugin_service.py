from constructs import Construct

from aws_cdk import (
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    BundlingOptions
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

        # this allows unit tests to skip the bundling process
        # which will attempt to write to /assets-output and
        # probably result in a PermissionError
        skip_bundling = self.node.try_get_context('skip_bundling')

        if skip_bundling:
            bundling_options = None
        else:
            bundling_options = BundlingOptions(
                    image=lambda_.Runtime.PYTHON_3_10.bundling_image,
                    command=[
                        'bash', '-c',
                        # Install dependencies into the 'python' directory
                        'pip install -r requirements.txt -t /asset-output/python'
                    ],
                )
        # Builds a lambda layer with Twilio of dependencies
        # It will read the requirements.txt file in the twilio_layer
        # directory and install everything needed. To synthesize this
        # locally, you will need to have a docker deamon running.

        twilio_layer = lambda_.LayerVersion(
            self, 'TwilioLayer',
            code=lambda_.Code.from_asset(
                'twilio_layer',
                bundling=bundling_options,
            ),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_10],
            description='This layer supplies the Twilio library',
        )

        messenger = lambda_.Function(
            self, "MessageHandler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset(
                'lambda_functions/',
                exclude=['subscriber_function/*', 'conftest.py'],
             ),
            layers=[twilio_layer],
            handler='message_function.index.handler',
            environment=dict(
                TABLE=table.table_name,
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
