import boto3

from botocore.exceptions import ClientError


class S3Provider:
    def __init__(self, region, stage):
        self.s3 = boto3.client("s3")
        self.bucket_name = f"perfect-projects-{stage}-{region}-storage"

    def upload_object_file(self, binary_file, file_key):
        try:
            self.s3.upload_fileobj(binary_file, self.bucket_name, file_key)
        except ClientError as error:
            print(error)
            return False
        return True

    def get_file(self, file_key):
        try:
            response = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=file_key)
        except ClientError as error:
            print(error)
            return False
        return response

    def delete_file(self, file_key):
        try:
            self.s3.delete_object(
                Bucket=self.bucket_name,
                Key=file_key)
        except ClientError as error:
            print(error)
            return False
        return True
