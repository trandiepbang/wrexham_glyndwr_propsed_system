import boto3

# Reference : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/client/create_platform_endpoint.html#create-platform-endpointhttps://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/client/create_platform_endpoint.html#create-platform-endpoint

def pushDataIntoNotificationAmazonSNS(message, target_arn, subject, region_name='ap-southeast-1', access_key='', secret_key=''):
    sns_client = boto3.client('sns',
                              region_name=region_name,
                              aws_access_key_id=access_key,
                              aws_secret_access_key=secret_key)
    
    response = sns_client.publish(
        TargetArn=target_arn,
        Message=message,
        Subject=subject
    )
    
    print("pushDataIntoNotificationAmazonSNS response ", response)
    return response

def storeLatestEndpointArn(token, region_name='ap-southeast-1', access_key='', secret_key='', platform_application_arn = ''):
    sns_client = boto3.client('sns', 
                       region_name=region_name,
                       aws_access_key_id=access_key,
                       aws_secret_access_key=secret_key)

    response = sns_client.create_platform_endpoint(
        PlatformApplicationArn=platform_application_arn,
        Token=token
    )

    return response['EndpointArn']
