"""
Form parser module
"""
import random
from os import remove
import string
from venv import logger
from storage_module import upload_to_bucket
import base64


def print_the_upload_form(data: dict):
    print("=" * 8, "Basic info about the employee:", "=" * 8)
    print("Name: ", data["name"])
    print("Employee ID: ", data["empId"])
    print("Location: ", data["location"])
    print("Designation: ", data["designation"])
    print("Department: ", data["department"])
    print("Purpose of Visit: ", data["purposeOfVisit"])
    print()
    print("=" * 8, "Travel details:", "=" * 8)
    print("Length of travels: ", len(data["travels"]))
    print()

    for c, i in enumerate(data["travels"]):
        print("=" * 8, "Travel #", c + 1, "=" * 8)
        print("Travel ID: ", i["travelId"])
        print("Travel date: ", i["travelDate"])
        print("Travel from: ", i["travelFrom"])
        print("Travel to: ", i["travelTo"])
        print("Travel mode: ", i["travelMode"])
        print("Travel class: ", i["travelClass"])
        print("Travel fare: ", i["travelFare"])
        print("Travel conveyance: ", i["travelConveyance"])
        print("Travel food and lodging: ", i["travelFoodLodging"])
        print("Travel incidental: ", i["travelIncidemtal"])
        print("Travel total: ", i["travelTotal"])
        print()
        print("=" * 8, "Travel details:", "=" * 8)
        print("Length of conveyances: ", len(i["travelDetails"]["conveyances"]))
        print("Length of food and lodgings: ", len(i["travelDetails"]["foodLodgings"]))
        print("Length of incidentals: ", len(i["travelDetails"]["incidentals"]))
        print()
        print("=" * 8, "Conveyances:", "=" * 8)
        for c, j in enumerate(i["travelDetails"]["conveyances"]):
            print("Conveyance #", c + 1)
            print("Conveyance ID: ", j["conveyanceId"])
            print("Conveyance date: ", j["conveyanceDate"])
            print("Conveyance from: ", j["conveyanceFrom"])
            print("Conveyance to: ", j["conveyanceTo"])
            print("Conveyance purpose: ", j["conveyancePurpose"])
            print("Conveyance amount: ", j["conveyanceAmount"])
            print("Conveyance bill: ", j["conveyanceBill"])
        print()
        print("=" * 8, "Food and Lodgings:", "=" * 8)
        for c, k in enumerate(i["travelDetails"]["foodLodgings"]):
            print("Food and Lodging #", c + 1)
            print("Food and Lodging ID: ", k["foodLodgingId"])
            print("Food and Lodging date: ", k["foodLodgingDate"])
            print("Food and Lodging bill no: ", k["foodLodgingBillNo"])
            print("Food and Lodging hotel: ", k["foodLodgingHotel"])
            print("Food and Lodging occupancy: ", k["foodLodgingOccupancy"])
            print("Food and Lodging amount: ", k["foodLodgingAmount"])
            print("Food and Lodging bill: ", k["foodLodgingBill"])
        print()
        print("=" * 8, "Incidentals:", "=" * 8)
        for c, l in enumerate(i["travelDetails"]["incidentals"]):
            print("Incidental #", c + 1)
            print("Incidental ID: ", l["incidentalId"])
            print("Incidental date: ", l["incidentalDate"])
            print("Incidental expense: ", l["incidentalExpense"])
            print("Incidental remarks: ", l["incidentalRemarks"])
            print("Incidental amount: ", l["incidentalAmount"])
            print("Incidental bill: ", l["incidentalBill"])


def generate_randome_string(N=8):
    return "".join(random.choices(string.ascii_letters + string.digits, k=N))


class FormParser:
    def __init__(self, data: dict, database):
        self.data = data
        self.database = database
        self.is_travel_upload = True

    def upload(self):
        self.upload_the_travels()

        return self.is_travel_upload

    def upload_bill(self, file_str: str):
        file_name = "uploaded-bills/" + generate_randome_string() + ".jpg"

        with open(file_name, "wb") as f:
            f.write(base64.b64decode(file_str))

        bill_id = upload_to_bucket(file_name)
        remove(file_name)

        return bill_id

    def upload_the_travels(self):
        for c, i in enumerate(self.data["travels"]):
            print("[+] Travel #", c + 1)

            new_data = {}

            new_data["empId"] = self.data["empId"]
            new_data["travelId"] = self.data["empId"] + "_" + generate_randome_string()
            new_data["travelDate"] = i["travelDate"]
            new_data["travelFrom"] = i["travelFrom"]
            new_data["travelTo"] = i["travelTo"]
            new_data["travelMode"] = i["travelMode"]
            new_data["travelClass"] = i["travelClass"]
            new_data["travelFare"] = i["travelFare"]
            new_data["travelConveyance"] = i["travelConveyance"]
            new_data["travelFoodLodging"] = i["travelFoodLodging"]
            new_data["travelIncidemtal"] = i["travelIncidemtal"]
            new_data["travelTotal"] = i["travelTotal"]

            self.upload_the_conveyances(i["travelDetails"]["conveyances"], new_data["travelId"])
            self.upload_the_food_lodgings(i["travelDetails"]["foodLodgings"], new_data["travelId"])
            self.upload_the_incidentals(i["travelDetails"]["incidentals"], new_data["travelId"])
            result = self.database.upload_the_travel(new_data)

            if result:
                print("[+] Travel details uploaded successfully")
                logger.info(f"[+] Travel details uploaded successfully for {self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("[+] Travel details failed to upload")
                logger.warning(f"[+] Travel details failed to upload for {self.data['empId']}")
                self.is_travel_upload *= False

    def upload_the_conveyances(self, data: list, travel_id: str):
        for c, i in enumerate(data):
            print("[+] Conveyance #", c + 1)

            bill_id = self.upload_bill(i["conveyanceBill"])

            new_data = {}
            new_data["conveyanceId"] = bill_id
            new_data["travelId"] = travel_id
            new_data["conveyanceDate"] = i["conveyanceDate"]
            new_data["conveyanceFrom"] = i["conveyanceFrom"]
            new_data["conveyanceTo"] = i["conveyanceTo"]
            new_data["conveyanceMode"] = i["conveyanceMode"]
            new_data["conveyancePurpose"] = i["conveyancePurpose"]
            new_data["conveyanceAmount"] = i["conveyanceAmount"]

            result = self.database.upload_the_conveyance(new_data)

            if result:
                print("[+] Conveyance details uploaded successfully")
                logger.info(f"[+] Conveyance details uploaded successfully for {self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("[+] Conveyance details failed to upload")
                logger.warning(f"[+] Conveyance details failed to upload for {self.data['empId']}")
                self.is_travel_upload *= False

    def upload_the_food_lodgings(self, data: list, travel_id: str):
        for c, i in enumerate(data):
            print("[+] Food and Lodging #", c + 1)

            bill_id = self.upload_bill(i["foodLodgingBill"])

            new_data = {}

            new_data["foodLodgingId"] = bill_id
            new_data["travelId"] = travel_id
            new_data["foodLodgingDate"] = i["foodLodgingDate"]
            new_data["foodLodgingBillNo"] = i["foodLodgingBillNo"]
            new_data["foodLodgingHotel"] = i["foodLodgingHotel"]
            new_data["foodLodgingOccupancy"] = i["foodLodgingOccupancy"]
            new_data["foodLodgingAmount"] = i["foodLodgingAmount"]

            result = self.database.upload_the_food_lodging(new_data)

            if result:
                print("[+] Food and Lodging details uploaded successfully")
                logger.info(f"[+] Food and Lodging details uploaded successfully for {self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("[+] Food and Lodging details failed to upload")
                logger.warning(f"[+] Food and Lodging details failed to upload for {self.data['empId']}")
                self.is_travel_upload *= False

    def upload_the_incidentals(self, data: list, travel_id: str):
        for c, i in enumerate(data):
            print("[+] Incidental #", c + 1)

            bill_id = self.upload_bill(i["incidentalBill"])

            new_data = {}

            new_data["incidentalId"] = bill_id
            new_data["travelId"] = travel_id
            new_data["incidentalDate"] = i["incidentalDate"]
            new_data["incidentalExpense"] = i["incidentalExpense"]
            new_data["incidentalRemarks"] = i["incidentalRemarks"]
            new_data["incidentalAmount"] = i["incidentalAmount"]

            result = self.database.upload_the_incidental(new_data)

            if result:
                print("[+] Incidental details uploaded successfully")
                logger.info(f"[+] Incidental details uploaded successfully for {self.data['empId']}")
                self.is_travel_upload *= True

            else:
                print("[+] Incidental details failed to upload")
                logger.warning(f"[+] Incidental details failed to upload for {self.data['empId']}")
                self.is_travel_upload *= False
