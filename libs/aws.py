import boto3


def send_push_notification(message, target_arn, subject, region_name='ap-southeast-1', access_key='', secret_key=''):
    sns_client = boto3.client('sns',
                              region_name=region_name,
                              aws_access_key_id=access_key,
                              aws_secret_access_key=secret_key)
    
    response = sns_client.publish(
        TargetArn=target_arn,
        Message=message,
        Subject=subject
    )
    
    print("send_push_notification response ", response)
    return response
