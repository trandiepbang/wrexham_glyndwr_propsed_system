import boto3


def send_push_notification(message, topic_arn, region_name='ap-southeast-1', access_key='AKIAUKGZUDFB43ZL6DX6', secret_key='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'):
    sns_client = boto3.client('sns',
                              region_name=region_name,
                              aws_access_key_id=access_key,
                              aws_secret_access_key=secret_key)
    
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
    
    return response

# # Usage
# response = send_push_notification("Hello from AWS SNS!", "arn:aws:sns:ap-southeast-1:296809142595:crime-notification")
# print(response)
