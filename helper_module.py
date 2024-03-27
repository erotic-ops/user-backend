import random
import string
from os import environ

import requests

from cache_module import Cache
from database_module import Database
from logging_module import logger
from storage_module import Storage

db_obj = Database()
storage_obj = Storage()
cache_obj = Cache()

def random_string(N=10):
    return "".join(random.choices(string.ascii_letters + string.digits, k=N))

def send_email(receivers: list[str], subject: str, message: str) -> bool:
    """Method to send email

    Return: True if email sent successfully
    """
    url = environ.get("NOTIFICATION_SERVER_URL", "")
    head = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {environ.get('AUTH_TOKEN')}"
    }
    json_data = {"receiver": receivers, "subject": subject, "message": message}

    response = requests.post(url, json=json_data, headers=head, timeout=5)
    print(response.text)
    return response.status_code == 200


def match_the_values(travel_ids: list) -> dict:
    """Method to match the values from the cache

    Return: Dictionary of values
    """

    for travel_id in travel_ids:
        all_bills = db_obj.get_all_bill_from_travel_id(travel_id)

        if all_bills is None or len(all_bills) == 0:
            print("No bills found")
            logger.warning(f"No bills found for {travel_id}")

            return False

        bill_ids = [i[0] for i in all_bills]
        bill_amounts = [i[1] for i in all_bills]

        cache_amounts = cache_obj.get_all_values(bill_ids)

        for bill_amount, cache_amount in zip(bill_amounts, cache_amounts):

            if bill_amount == cache_amount:
                print("Same amount", bill_amount, cache_amount)

            else:
                print("Different amount", bill_amount, cache_amount)


class FormParser:
    def __init__(self, data: dict):
        self.data = data
        self.is_travel_upload = True

    def generate_random_string(self, N=8):
        return "".join(random.choices(string.ascii_letters + string.digits, k=N))

    def upload_the_travels(self):
        travel_ids = []

        for c, i in enumerate(self.data["travels"]):
            travel_id = self.data["empId"] + \
                "_" + self.generate_random_string()
            travel_ids.append(travel_id)

            print("Travel #", c + 1)

            new_data = {
                "empId": self.data["empId"],
                "travelId": travel_id,
                "travelDate": i["travelDate"],
                "travelFrom": i["travelFrom"],
                "travelTo": i["travelTo"],
                "travelMode": i["travelMode"],
                "travelClass": i["travelClass"],
                "travelFare": i["travelFare"],
                "travelConveyance": i["travelConveyance"],
                "travelFoodLodging": i["travelFoodLodging"],
                "travelIncidental": i["travelIncidental"],
                "travelTotal": i["travelTotal"],
            }

            self.upload_the_conveyances(
                i["travelDetails"]["conveyances"], new_data["travelId"])
            self.upload_the_food_lodgings(
                i["travelDetails"]["foodLodgings"], new_data["travelId"])
            self.upload_the_incidentals(
                i["travelDetails"]["incidentals"], new_data["travelId"])

            if db_obj.upload_the_travel(new_data):
                print("Travel details uploaded successfully")
                logger.info(f"Travel details uploaded successfully for {
                            self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("Travel details failed to upload")
                logger.warning(f"Travel details failed to upload for {
                               self.data['empId']}")
                self.is_travel_upload *= False

        return self.is_travel_upload, travel_ids

    def upload_the_conveyances(self, data: list, travel_id: str):
        for c, i in enumerate(data):
            print("Conveyance #", c + 1)

            bill_id = random_string()

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
                logger.info(f"Conveyance details uploaded successfully for {
                            self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("Conveyance details failed to upload")
                logger.warning(f"Conveyance details failed to upload for {
                               self.data['empId']}")
                self.is_travel_upload *= False

    def upload_the_food_lodgings(self, data: list, travel_id: str):
        for c, i in enumerate(data):
            print("Food and Lodging #", c + 1)
            
            bill_id = random_string()
            
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
                logger.info(f"Food and Lodging details uploaded successfully for {
                            self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("Food and Lodging details failed to upload")
                logger.warning(f"Food and Lodging details failed to upload for {
                               self.data['empId']}")
                self.is_travel_upload *= False

    def upload_the_incidentals(self, data: list, travel_id: str):
        for c, i in enumerate(data):
            print("Incidental #", c + 1)

            bill_id = random_string()

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
                logger.info(f"Incidental details uploaded successfully for {
                            self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("Incidental details failed to upload")
                logger.warning(f"Incidental details failed to upload for {
                               self.data['empId']}")
                self.is_travel_upload *= False
