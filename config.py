import os

region_name=os.environ.get('AWS_REGION', 'ap-southeast-1')
aws_access_key_id=os.environ.get('AWS_ACCESS_KEY', '')
aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', '')
platform_application_arn = os.environ.get('PLATFORM_APPLICATION_ARN', '')
