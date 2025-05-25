import os
import boto3
from botocore.client import Config
from boto3.s3.transfer import S3Transfer

class UploadStac:
    session = None
    client = None
    
    def __init__(self):
        self.session = boto3.session.Session()
        self.client = self.session.client(
            "s3",
            region_name=os.environ['REGION'],
            endpoint_url=os.environ['SPACE_URL'],
            aws_access_key_id=os.environ['ACCESS_KEY'],
            aws_secret_access_key=os.environ['SECRET_KEY'],
            config=Config(signature_version='s3v4')
        )
        
    def upload_catalog(self, catalog_name, local_catalog_path):
        key = f"{catalog_name}/"
        bucket_name = 'stac-catalogs' 
        bucket_file = os.path.join(key, os.path.basename(local_catalog_path))

        # Creates directory based on the catalog_name
        self.client.put_object(Bucket=bucket_name, Body='', Key=key)
        # Adds the catalog.json to the directory.
        self.client.upload_file(local_catalog_path, bucket_name, 
            bucket_file, ExtraArgs={'ACL':'public-read'})
        
    def upload_collection(self, collection_bucket_path, local_collection_path):
        key = f'{collection_bucket_path}/'
        bucket_name = 'stac-catalogs' 
        bucket_file = os.path.join(key, os.path.basename(local_collection_path))
        
        self.client.put_object(Bucket=bucket_name, Body='', Key=key)
        self.client.upload_file(local_collection_path, bucket_name, 
            bucket_file, ExtraArgs={'ACL':'public-read'})

    def upload_item(self, item_bucket_path, local_item_path):
        key = f'{item_bucket_path}/'
        bucket_name = 'stac-catalogs' 
        bucket_file = os.path.join(key, os.path.basename(local_item_path))

        self.client.put_object(Bucket=bucket_name, Body='', Key=key)
        self.client.upload_file(local_item_path,
            bucket_name, bucket_file, ExtraArgs={'ACL':'public-read'})
