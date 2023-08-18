import boto3


def send_push_notification(message, topic_arn, region_name='us-west-2', access_key='YOUR_ACCESS_KEY', secret_key='YOUR_SECRET_KEY'):
    sns_client = boto3.client('sns',
                              region_name=region_name,
                              aws_access_key_id=access_key,
                              aws_secret_access_key=secret_key)
    
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
    
    return response

# Usage
response = send_push_notification("Hello from AWS SNS!", "arn:aws:sns:us-west-2:123456789012:YourTopicName")
print(response)
