import random
import string
from os import environ

import requests
from flask import Flask, jsonify, request

from database_module import Database
from logging_module import logger
from storage_module import Storage

app = Flask(__name__)

# ====== Environment Variables ======
AUTH_TOKEN = environ.get("AUTH_TOKEN")
NOTIFICATION_SERVER = environ.get("NOTIFICATION_SERVER_URL")
app.secret_key = AUTH_TOKEN

# ====== Helper Class ======
class FormParser:
    def __init__(self, data: dict):
        self.data = data
        self.is_travel_upload = True

    def generate_random_string(self, N=8):
        return "".join(random.choices(string.ascii_letters + string.digits, k=N))

    def upload_the_travels(self):
        for c, i in enumerate(self.data["travels"]):
            print("Travel #", c + 1)

            new_data = {
                "empId": self.data["empId"],
                "travelId": self.data["empId"] + "_" + self.generate_random_string(5),
                "travelDate": i["travelDate"],
                "travelFrom": i["travelFrom"],
                "travelTo": i["travelTo"],
                "travelMode": i["travelMode"],
                "travelClass": i["travelClass"],
                "travelFare": i["travelFare"],
                "travelConveyance": i["travelConveyance"],
                "travelFoodLodging": i["travelFoodLodging"],
                "travelIncidemtal": i["travelIncidemtal"],
                "travelTotal": i["travelTotal"],
            }

            self.upload_the_conveyances(i["travelDetails"]["conveyances"], new_data["travelId"])
            self.upload_the_food_lodgings(i["travelDetails"]["foodLodgings"], new_data["travelId"])
            self.upload_the_incidentals(i["travelDetails"]["incidentals"], new_data["travelId"])

            if db_obj.upload_the_travel(new_data):
                print("Travel details uploaded successfully")
                logger.info(f"Travel details uploaded successfully for {self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("Travel details failed to upload")
                logger.warning(f"Travel details failed to upload for {self.data['empId']}")
                self.is_travel_upload *= False

        return self.is_travel_upload

    def upload_the_conveyances(self, data: list, travel_id: str):
        for c, i in enumerate(data):
            print("Conveyance #", c + 1)

            bill_id = storage_obj.upload_image(i["conveyanceBill"])

            new_data = {
                "conveyanceId": bill_id,
                "travelId": travel_id,
                "conveyanceDate": i["conveyanceDate"],
                "conveyanceFrom": i["conveyanceFrom"],
                "conveyanceTo": i["conveyanceTo"],
                "conveyanceMode": i["conveyanceMode"],
                "conveyancePurpose": i["conveyancePurpose"],
                "conveyanceAmount": i["conveyanceAmount"],
            }
            if db_obj.upload_the_conveyance(new_data):
                print("Conveyance details uploaded successfully")
                logger.info(f"Conveyance details uploaded successfully for {self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("Conveyance details failed to upload")
                logger.warning(f"Conveyance details failed to upload for {self.data['empId']}")
                self.is_travel_upload *= False

    def upload_the_food_lodgings(self, data: list, travel_id: str):
        for c, i in enumerate(data):
            print("Food and Lodging #", c + 1)

            bill_id = storage_obj.upload_image(i["foodLodgingBill"])

            new_data = {
                "foodLodgingId": bill_id,
                "travelId": travel_id,
                "foodLodgingDate": i["foodLodgingDate"],
                "foodLodgingBillNo": i["foodLodgingBillNo"],
                "foodLodgingHotel": i["foodLodgingHotel"],
                "foodLodgingOccupancy": i["foodLodgingOccupancy"],
                "foodLodgingAmount": i["foodLodgingAmount"],
            }

            if db_obj.upload_the_food_lodging(new_data):
                print("Food and Lodging details uploaded successfully")
                logger.info(f"Food and Lodging details uploaded successfully for {self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("Food and Lodging details failed to upload")
                logger.warning(f"Food and Lodging details failed to upload for {self.data['empId']}")
                self.is_travel_upload *= False

    def upload_the_incidentals(self, data: list, travel_id: str):
        for c, i in enumerate(data):
            print("Incidental #", c + 1)

            bill_id = storage_obj.upload_image(i["incidentalBill"])

            new_data = {
                "incidentalId": bill_id,
                "travelId": travel_id,
                "incidentalDate": i["incidentalDate"],
                "incidentalExpense": i["incidentalExpense"],
                "incidentalRemarks": i["incidentalRemarks"],
                "incidentalAmount": i["incidentalAmount"],
            }

            if db_obj.upload_the_incidental(new_data):
                print("Incidental details uploaded successfully")
                logger.info(f"Incidental details uploaded successfully for {self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("Incidental details failed to upload")
                logger.warning(f"Incidental details failed to upload for {self.data['empId']}")
                self.is_travel_upload *= False


class Notification:
    """Notification class to send the email and SMS to the user"""

    def __init__(self) -> None:
        """
        Keyword arguments:
        subject -- Subject of the message
        receivers -- List of receivers
        message -- Message to be sent
        """
        # self.subject = subject
        # self.receivers = receivers
        # self.message = message

    def send_email(self, subject: str, receivers: list, message: str) -> bool:
        """Method to send the message to the user

        Return: True if the message is sent successfully else False
        """

        req_headers = {"Authorization": f"Bearer {AUTH_TOKEN}", "Content-Type": "application/json"}
        json_message = {"subject": subject, "receiver": receivers, "message": message}
        response = requests.post(
            url=f"{NOTIFICATION_SERVER}/email",
            json=json_message,
            headers=req_headers,
        )

        print(response.status_code)
        print(response.text)

        # return response.json()["status"] == "success"


# ====== App routes ======

@app.route("/")
def home_page():
    return "Hello World!"


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

    if form.upload_the_travels():
        Notification().send_email("Form uploaded successfully", ["hm0092374@gmail.com"], "Form uploaded successfully")
        msg = {"status": "success", "message": "Form data uploaded successfully"}
        logger.info(f"Form data uploaded successfully for {request.json['empId']}")

        return jsonify(msg), 200

    Notification().send_email("Form failed to upload", ["hm0092374@gmail.com"], "Form failed to upload")
    msg = {"status": "failure", "message": "Form data failed to upload"}
    logger.warning(f"Form data failed to upload for {request.json['empId']}")

    return jsonify(msg), 500


if __name__ == "__main__":
    db_obj = Database()
    storage_obj = Storage()

    if db_obj.is_db_connected():
        app.run(debug=True, host="0.0.0.0", port=5000)
        db_obj.disconnect()
