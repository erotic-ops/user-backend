from os import environ, remove
from flask import Flask, request, redirect

from appwrite import client
from appwrite import input_file
from appwrite.services import storage
from appwrite.id import ID


if 'APPWRITE_PROJECT_ID' not in environ:
    print('[+] Must set all environment variables')
    exit()
    
app = Flask(__name__)
client_app = client.Client()

client_app = (
    client_app.set_endpoint("https://cloud.appwrite.io/v1")
    .set_project(environ.get("APPWRITE_PROJECT_ID").strip())
    .set_key(environ.get("APPWRITE_API_KEY").strip())
)
storage_app = storage.Storage(client_app)


def upload_to_bucket(file_name: str):
    result = storage_app.create_file(
        environ.get("APPWRITE_BUCKET_ID").strip(),
        ID.unique(),
        input_file.InputFile.from_path("uploaded-bills/" + file_name)
    )

    print(result)

@app.route("/")
def home_page():
    return "Hello World!"


@app.route("/upload", methods=["POST"])
def upload_form_data():
    for upload_file in request.files.getlist("fileToUpload"):
        upload_file.save("uploaded-bills/" + upload_file.filename)
        
        upload_to_bucket(upload_file.filename)
        
        remove("uploaded-bills/" + upload_file.filename)

    print(request.form)

    return redirect("http://127.0.0.1:8000/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
