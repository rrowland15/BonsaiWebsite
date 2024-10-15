from google.cloud import storage
import os

credential_path = "credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def create_bucket(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    #bucket.location = 'US'
    bucket = storage_client.create_bucket(bucket)
    vars(bucket)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name) # destination blob name can have a folder created by document/newfilename

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def check_bucket(bucket_name):
    storage_client = storage.Client()
    my_bucket = storage_client.get_bucket(bucket_name)

def download_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name) # destination blob name can have a folder created by document/newfilename

    with open(source_file_name,'wb') as f:
        storage_client.download_blob_to_file(blob,f)


    print(f"File {source_file_name} donwloaded from {destination_blob_name}.")


#Example usage create_bucket:
#create_bucket("tree_test")

# Example usage upload_blob
bucket_name = "treephotos"
source_file_name = "/Users/ryanrowland/Desktop/gingko.jpg"
destination_blob_name = "gingkoleaf"
upload_blob(bucket_name, source_file_name, destination_blob_name)

#Example usage of download_blob
#download_blob('tree_images',os.path.join(os.getcwd(),'file1.jpg'),'little_tree')
#print(os.getcwd())