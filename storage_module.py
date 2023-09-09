from os import environ, mkdir, remove
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

# Make the directory if it doesn't exist
try:
    mkdir("uploaded-bills")
except FileExistsError:
    pass


class Storage:
    def __init__(self):
        client_app = client.Client()
        client_app = client_app.set_endpoint("https://cloud.appwrite.io/v1").set_project(APPWRITE_PROJECT_ID).set_key(APPWRITE_API_KEY)
        self.storage_app = storage.Storage(client_app)

    def generate_random_string(self, N=8):
        return "".join(random.choices(string.ascii_letters + string.digits, k=N))

    def upload_image(self, file_str: str):
        file_name = f"uploaded-bills/{self.generate_random_string()}.jpg"

        with open(file_name, "wb") as f:
            f.write(base64.b64decode(file_str))

        bill_id = self.__upload(file_name)
        remove(file_name)

        return bill_id

    def __upload(self, file_path: str):
        result = self.storage_app.create_file(
            APPWRITE_BUCKET_ID,
            ID.unique(),
            input_file.InputFile.from_path(file_path),
        )

        return result["$id"]


if __name__ == "__main__":
    s = Storage()
    print(s._Storage__upload(r"C:\Users\Harshit Music\Pictures\h.jpg"))
