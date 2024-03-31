from os import environ
from threading import Thread

from flask import Flask, jsonify, request

from modules.logging_module import logger
from modules.database_module import Database
from modules.helper_module import FormParser, send_email

# Importing all environment variables
# Windows: FOR /F "eol=# tokens=*" %i IN (.env) DO SET %i
# Linux: export $(cat .env | grep -v # | xargs)
# Mac: export $(cat .env | grep -v # | xargs)


# ====== Initial Flask App ======
app = Flask(__name__)
app.secret_key = environ.get("AUTH_TOKEN")


# ====== App routes ======
@app.route("/", methods=["GET"])
def home_page():
    return jsonify({"status": "success", "message": "Welcome to the user backend"})


@app.route("/upload", methods=["POST"])
def upload_form_data():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header:
        msg = {"status": "failure", "message": "No Authorization header found"}
        logger.warning("No Authorization header found")

        return jsonify(msg), 401

    __token = auth_header.split(" ")[1]

    if __token != environ.get("AUTH_TOKEN"):
        msg = {"status": "failure", "message": "Invalid token"}
        logger.warning("Invalid token")

        return jsonify(msg), 401

    print("Method", request.method)
    print("Values", request.values)
    print("Path", request.path)
    print("Files", request.files)
    print("Form", request.form)
    print("Data", request.data)
    # print("Json", request.json)
    print("Headers", request.headers)
    print("Args", request.args)

    try:

        print("Employee ID:", request.json["empId"])
        form = FormParser(db_obj)

        travel_status, travel_ids = form.upload_the_travels(data=request.json)
        if travel_status:

            print('travel_ids', travel_ids)

            # bill_status = match_the_values(travel_ids)
            # print('bill_status', bill_status)

            Thread(target=send_email, args=(["hm0092374@gmail.com"], "Form uploaded successfully", "Form uploaded successfully")).start()
            msg = {"status": "success", "message": "Form data uploaded successfully"}
            logger.info(f"Form data uploaded successfully for {
                        request.json['empId']}")

            return jsonify(msg), 200

        Thread(target=send_email, args=(["hm0092374@gmail.com"], "Form failed to upload", "Form failed to upload")).start()
        msg = {"status": "failure", "message": "Form data failed to upload"}
        logger.warning(f"Form data failed to upload for {request.json['empId']}")

        return jsonify(msg), 500

    except Exception as e:
        print("Exception", type(e).__name__, e)
        logger.error(f"Exception occurred: {e}")

        return jsonify({"status": "failure", "message": f"Exception occurred: {e}"}), 400


db_obj = Database()
# storage_obj = Storage()
# cache_obj = Cache()

if db_obj.is_db_connected():
    print("Database connected successfully")
    logger.info("Database connected successfully")

else:
    print("Database failed to connect")
    logger.warning("Database failed to connect")
    exit()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
