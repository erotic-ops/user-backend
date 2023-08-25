from os import mkdir

from flask import Flask, jsonify, request

from database_module import Database
from form_parser import FormParser
from logging_module import logger
from email_module import send_the_email

app = Flask(__name__)

# Make the directory if it doesn't exist
try:
    mkdir("uploaded-bills")
except FileExistsError:
    pass


@app.route("/")
def home_page():
    return "Hello World!"


@app.route("/upload", methods=["POST"])
def upload_form_data():
    if request.headers.get("Content-Type") == "application/json":
        print("[+] Employee ID:", request.json["empId"])

        form = FormParser(data=request.json, database=db)
        result = form.upload()

        if result:
            send_the_email("Form uploaded successfully", "hm0092374@gmail.com")
            msg = {"status": "success", "message": "Form data uploaded successfully"}
            logger.info(f"[+] Form data uploaded successfully for {request.json['empId']}")

        else:
            send_the_email("Form failed to upload", "hm0092374@gmail.com")
            msg = {"status": "failure", "message": "Form data failed to upload"}
            logger.warning(f"[+] Form data failed to upload for {request.json['empId']}")

    else:
        msg = {"status": "failure", "message": "Invalid Content-Type"}
        logger.warning("[+] Invalid Content-Type")

    return jsonify(msg)


if __name__ == "__main__":
    db = Database()

    if db.is_db_connected():
        app.run(debug=True, host="0.0.0.0", port=5000)
        db.disconnect()
