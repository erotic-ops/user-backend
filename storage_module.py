from os import environ
import base64
import random
import string

from appwrite import client
from appwrite import input_file
from appwrite.services import storage
from appwrite.id import ID

# ====== Environment Variables ======
APPWRITE_PROJECT_ID = environ.get("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = environ.get("APPWRITE_API_KEY")
APPWRITE_BUCKET_ID = environ.get("APPWRITE_BUCKET_ID")


class Storage:
    def __init__(self):
        client_app = client.Client()
        client_app = client_app.set_endpoint("https://cloud.appwrite.io/v1").set_project(APPWRITE_PROJECT_ID).set_key(APPWRITE_API_KEY)
        self.storage_app = storage.Storage(client_app)

    def generate_random_string(self, N=8):
        return "".join(random.choices(string.ascii_letters + string.digits, k=N))

    def upload_image(self, file_str: str) -> str:
        file_name = f"{self.generate_random_string()}.jpg"
        file_data = base64.b64decode(file_str)

        result = self.storage_app.create_file(APPWRITE_BUCKET_ID, ID.unique(), input_file.InputFile.from_bytes(file_data, file_name, "image/jpeg"))

        return result["$id"]


if __name__ == "__main__":
    s = Storage()
    print(s.upload_image(r"C:\Users\Harshit Music\Pictures\1692199673102.jpg"))
