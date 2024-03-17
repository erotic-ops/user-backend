from os import environ
from threading import Thread

import requests
from flask import Flask, jsonify, request

from cache_module import Cache
from database_module import Database
from logging_module import logger
from storage_module import Storage
from helper_module import FormParser, match_the_values

# Importing all environment variables
# Windows: FOR /F "eol=# tokens=*" %i IN (.env) DO SET %i
# Linux: export $(cat .env | grep -v # | xargs)
# Mac: export $(cat .env | grep -v # | xargs)


# ====== Environment Variables ======
AUTH_TOKEN = environ.get("AUTH_TOKEN")
NOTIFICATION_SERVER = environ.get("NOTIFICATION_SERVER_URL")

# ====== Initial Flask App ======
app = Flask(__name__)
app.secret_key = AUTH_TOKEN


# ====== App routes ======

@app.route("/")
def home_page():
    return jsonify({"status": "success", "message": "Welcome to the user backend"})


@app.post("/upload")
def upload_form_data():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        msg = {"status": "failure", "message": "No Authorization header found"}
        logger.warning("No Authorization header found")

        return jsonify(msg), 401

    __token = auth_header.split(" ")[1]

    if __token != AUTH_TOKEN:
        msg = {"status": "failure", "message": "Invalid token"}
        logger.warning("Invalid token")

        return jsonify(msg), 401

    print("Employee ID:", request.json["empId"])

    form = FormParser(data=request.json)

    travel_status, travel_ids = form.upload_the_travels()
    if travel_status:

        print('travel_ids', travel_ids)

        bill_status = match_the_values(travel_ids)
        print('bill_status', bill_status)

        # Thread(target=Notification.send_email, args=("Form uploaded successfully", ["hm0092374@gmail.com"], "Form uploaded successfully")).start()
        msg = {"status": "success", "message": "Form data uploaded successfully"}
        logger.info(f"Form data uploaded successfully for {
                    request.json['empId']}")

        return jsonify(msg), 200

    # Thread(target=Notification.send_email, args=("Form failed to upload", ["hm0092374@gmail.com"], "Form failed to upload")).start()
    msg = {"status": "failure", "message": "Form data failed to upload"}
    logger.warning(f"Form data failed to upload for {request.json['empId']}")

    return jsonify(msg), 500


db_obj = Database()
storage_obj = Storage()
cache_obj = Cache()

if db_obj.is_db_connected():
    print("Database connected successfully")
    logger.info("Database connected successfully")

else:
    print("Database failed to connect")
    logger.warning("Database failed to connect")
    exit()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    db_obj.disconnect()
