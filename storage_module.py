from os import environ

from appwrite import client
from appwrite import input_file
from appwrite.services import storage
from appwrite.id import ID

if "APPWRITE_PROJECT_ID" not in environ:
    print("[+] Must set all environment variables")
    exit()

APPWRITE_PROJECT_ID = environ.get("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = environ.get("APPWRITE_API_KEY")
APPWRITE_BUCKET_ID = environ.get("APPWRITE_BUCKET_ID")

client_app = client.Client()

client_app = (
    client_app.set_endpoint("https://cloud.appwrite.io/v1")
    .set_project(APPWRITE_PROJECT_ID)
    .set_key(APPWRITE_API_KEY)
)
storage_app = storage.Storage(client_app)


def upload_to_bucket(file_name: str):
    result = storage_app.create_file(
        APPWRITE_BUCKET_ID,
        ID.unique(),
        input_file.InputFile.from_path(file_name),
    )

    return result
