from wikipedia_extract import get_wikipedia_data, extract_stadium_data
from google.cloud import storage
import pandas as pd
import io

def upload_to_gcs(data, bucket_name, file_name):
    """
    Uploads  data to Google Cloud Storage as a CSV file
    
    Parameters:
        data: The DataFrame to be uploaded.
        bucket_name : Name of the Google Cloud Storage bucket.
        file_name: Name of the CSV file to be created.
    
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Convert DataFrame to CSV format and then to bytes
    csv_data = data.to_csv(index=False)
    csv_bytes = csv_data.encode('utf-8')

    # Upload the CSV to GCS
    blob.upload_from_string(csv_data, content_type='text/csv')

    print(f"File {file_name} uploaded to {bucket_name} bucket.")

def main():
    # URL of the Wikipedia page containing stadium data
    wikipedia_url = 'https://es.wikipedia.org/wiki/Anexo:Estadios_de_f%C3%BAtbol_de_Am%C3%A9rica_del_Sur'

    html_content = get_wikipedia_data(wikipedia_url)

    if html_content:
        # Extract stadium data
        stadium_data = extract_stadium_data(html_content)

        df = pd.DataFrame(stadium_data)

        # Define GCS bucket and file name
        gcs_bucket = 'stadiums_bucket'
        gcs_file_name = 'southamerica_stadiums.csv'

        # Upload data to GCS
        upload_to_gcs(df, gcs_bucket, gcs_file_name)
        

    else:
        print('Failed to retrieve data from Wikipedia')

if __name__ == "__main__":
    main()
