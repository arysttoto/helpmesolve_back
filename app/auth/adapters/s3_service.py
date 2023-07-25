from typing import BinaryIO
from pydantic import BaseSettings
import os
from app.config import env

import boto3

aws_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_key = os.getenv("AWS_SECRET_ACCESS_KEY")


class S3Service:
    def __init__(self):
        self.s3 = boto3.client(
            "s3", aws_access_key_id=aws_id, aws_secret_access_key=aws_key
        )

    def upload_file(self, file: BinaryIO, filename: str):
        bucket = "aryst.toto-bucket"
        filekey = f"users/{filename}"

        self.s3.upload_fileobj(file, bucket, filekey)

        bucket_location = boto3.client(
            "s3", aws_access_key_id=aws_id, aws_secret_access_key=aws_key
        ).get_bucket_location(Bucket=bucket)
        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location["LocationConstraint"], bucket, filekey
        )

        return object_url

    def delete_file(self, filename):
        bucket = "aryst.toto-bucket"
        filekey = f"users/{filename.split('/')[-1]}"
        self.s3.delete_object(Bucket=bucket, Key=filekey)
