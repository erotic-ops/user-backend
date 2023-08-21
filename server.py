from os import mkdir, remove

from flask import Flask, jsonify, request

# from storage_module import upload_to_bucket

import random
import string
from database_module import Database

from form_parser import FormParser

app = Flask(__name__)

# Make the directory if it doesn't exist
try:
    mkdir("uploaded-bills")
except FileExistsError:
    pass



# def form_parser(data: dict):
#     for c, i in enumerate(data["travels"]):
#         travel_id = data["empId"] + "_" + generate_randome_string()


@app.route("/")
def home_page():
    return "Hello World!"


@app.route("/upload", methods=["POST"])
def upload_form_data():
    if request.headers.get("Content-Type") == "application/json":
        form = FormParser(request.json, database=db)
        result = form.upload()
        
        if result:
            msg = {"status": "success", "message": "Form data uploaded successfully"}
        else:
            msg = {"status": "failure", "message": "Form data failed to upload"}

    else:
        msg = {"status": "failure", "message": "Invalid Content-Type"}
        
    return jsonify(msg)



if __name__ == "__main__":
    db = Database()

    if db.is_db_connected():
        app.run(debug=True, host="0.0.0.0", port=5000)
        db.disconnect()
        
    else:
        print("[+] Database is not connected")
