import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.plugin_service_stack import PluginStack


# example tests. To run these tests, uncomment this file along with the example
# resource in my_widget_service/my_widget_service_stack.py
def test_dynamodb_table_created():
    app = core.App(context={'skip_bundling': True})
    stack = PluginStack(app, "plugin-service")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::DynamoDB::Table", {
        "KeySchema": [
            {
                "AttributeName": "phone_number",
                "KeyType": "HASH"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "phone_number",
                "AttributeType": "S"
            }
        ]
    })
