import os
import json
import base64
import boto3
import pandas as pd


s3_client = boto3.resource("s3")
s3_bucket_name = "google-trends-search"


def lambda_handler(event: dict, context) -> None:
    for record in event['Records']:
        try:
            print(f"Processed Kinesis Event - EventID: {record['eventID']}")
            record_data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            print(f"Record Data: {record_data}")
            # TODO: Do interesting work based on the new data
        except Exception as e:
            print(f"An error occurred {e}")
            raise e
    print(f"Successfully processed {len(event['Records'])} records.")