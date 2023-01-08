import boto3
import os
AWS_ACCESS_KEY_ID = os.getenv('AKIAVZH4SBSYYMPKMY7W')
AWS_SECRET_ACCESS_KEY = os.getenv('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')
AWS_REGION = os.getenv('eu-west-1')
AWS_BUCKET_NAME = os.getenv('bucketeer-65ac7f07-6d84-42b2-9cec-88ead6098ad0')


s3 = boto3.client(
    's3',
    region_name='eu-west-1',
    aws_access_key_id="AKIAVZH4SBSYYMPKMY7W",
    aws_secret_access_key='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',
)
#for bucket in s3.buckets.all():
#    print(bucket.name)


filename='static/images/spotify_logo.png'
#if os.path.exists(filename):
#    s3.upload_file(Filename=filename, Bucket='bucketeer-65ac7f07-6d84-42b2-9cec-88ead6098ad0', Key='public/spotify_logo.png')

for key in s3.list_objects(Bucket='bucketeer-65ac7f07-6d84-42b2-9cec-88ead6098ad0')['Contents']:
    print(key['Key'])