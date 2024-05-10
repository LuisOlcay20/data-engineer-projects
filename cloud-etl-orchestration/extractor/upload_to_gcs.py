from google.cloud import storage

def upload_to_gcs(file_name, bucket_name):
    """
    Uploads a CSV file to Google Cloud Storage.
    
    Parameters:
        file_name: Name of the CSV file to be uploaded.
        bucket_name: Name of the Google Cloud Storage bucket.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(filename=file_name, content_type='text/csv')
    print(f"File {file_name} uploaded to {bucket_name} bucket.")