import boto3

def copyLocalFileToS3(filename, bucketName="jsimon-public"):
    boto3.client('s3').upload_file(filename, bucketName, filename)
