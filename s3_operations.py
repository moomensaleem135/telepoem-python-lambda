import io
import boto3
import pandas as pd
import os
import traceback


def read_excel_from_s3(file_name=None):
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket_name = os.getenv('BUCKET_NAME')

    if not all([aws_access_key_id, aws_secret_access_key, bucket_name, file_name]):
        raise ValueError("AWS credentials or S3 bucket/file information not provided.")

    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file_name)
        excel_data = pd.read_excel(io.BytesIO(obj['Body'].read()), sheet_name=None,
                                   engine='openpyxl')  # Read all sheets into a dictionary
        return excel_data
    except FileNotFoundError:
        raise RuntimeError("The specified file was not found on S3.")
    except Exception as e:
        raise RuntimeError(f"Failed to read Excel file from S3: {str(e)}\n{traceback.format_exc()}")
