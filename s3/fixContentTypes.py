import boto3
from mimetypes import guess_type

# Initialize a session using Amazon S3
s3 = boto3.client('s3')

# Specify your bucket name
bucket_name = 'morelibertynow.com'


def update_content_type(bucket):
    # List all objects within the bucket
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket):
        if 'Contents' not in page:
            continue
        for obj in page['Contents']:
            key = obj['Key']
            # Guess the file's content type
            content_type = guess_type(key)[0]
            if content_type:
                print(f'Updating {key} to {content_type}')
                # Copy the object to itself in S3, updating the metadata
                s3.copy_object(Bucket=bucket, Key=key, CopySource={'Bucket': bucket, 'Key': key},
                               MetadataDirective='REPLACE',
                               ContentType=content_type)
            else:
                print(f'Could not determine content type for {key}')


# Update the Content-Type for all objects in the specified bucket
update_content_type(bucket_name)
