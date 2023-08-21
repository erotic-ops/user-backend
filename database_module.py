import threading
from os import environ

import mysql.connector

if "DB_HOST" not in environ:
    print("[+] DB_HOST not found in the environment variables")
    exit(1)

db_lock = threading.RLock()


class Database:
    """
    The database class to connect to the database
    """

    def __init__(self):
        try:
            self.__connection = mysql.connector.connect(
                host=environ.get("DB_HOST"),
                user=environ.get("DB_USER"),
                password=environ.get("DB_PASSWORD"),
                database=environ.get("DB_DATABASE"),
                autocommit=True,
            )
            self.__cursor = self.__connection.cursor()
            print("[+] Connected to the database")

        except mysql.connector.Error as e:
            print("[+] An error occurred", e)

    def is_db_connected(self):
        return self.__connection.is_connected()
        
    def disconnect(self):
        self.__connection.close()
        self.__cursor.close()
        print("[+] Disconnected from the database")

    def upload_the_travel(self, data: dict):
        """
        Upload the travel details in the travel table
        """

        db_lock.acquire()

        try:
            self.__cursor.execute(
                "INSERT INTO travel VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data["empId"],
                    data["travelId"],
                    data["travelDate"],
                    data["travelFrom"],
                    data["travelTo"],
                    data["travelMode"],
                    data["travelClass"],
                    data["travelFare"],
                    data["travelConveyance"],
                    data["travelFoodLodging"],
                    data["travelIncidemtal"],
                    data["travelTotal"],
                )
            )
            self.__connection.commit()

        except mysql.connector.Error as e:
            print("[+] An error occurred while uploading the travel details", e)
            db_lock.release()
            return False
        
        else:
            db_lock.release()
            return True
        
    
    def upload_the_conveyance(self, data: dict):
        """
        Upload the conveyance details in the conveyance table
        """
        
        db_lock.acquire()
        
        try:
            self.__cursor.execute(
                "INSERT INTO conveyance VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    data["conveyanceId"],
                    data["conveyanceDate"],
                    data["conveyanceFrom"],
                    data["conveyanceTo"],
                    data["conveyanceMode"],
                    data["conveyancePurpose"],
                    data["conveyanceAmount"]
                )
            )
            self.__connection.commit()
            
        except mysql.connector.Error as e:
            print("[+] An error occurred while uploading the conveyance details", e)
            db_lock.release()
            return False

        else:
            db_lock.release()
            return True
        
    def upload_the_food_lodging(self, data: dict):
        """
        Upload the food and lodging details in the food_lodging table
        """
        
        db_lock.acquire()
        
        try:
            self.__cursor.execute(
                "INSERT INTO food_lodging VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    data["foodLodgingId"],
                    data["foodLodgingDate"],
                    data["foodLodgingBillNo"],
                    data["foodLodgingHotel"],
                    data["foodLodgingOccupancy"],
                    data["foodLodgingAmount"]
                )
            )
            self.__connection.commit()
            
        except mysql.connector.Error as e:
            print("[+] An error occurred while uploading the food and lodging details", e)
            db_lock.release()
            return False

        else:
            db_lock.release()
            return True
        
    def upload_the_incidental(self, data: dict):
        """
        Upload the incidental details in the incidental table
        """
        
        db_lock.acquire()
        
        try:
            self.__cursor.execute(
                "INSERT INTO incidental VALUES (%s, %s, %s, %s, %s)",
                (
                    data["incidentalId"],
                    data["incidentalDate"],
                    data["incidentalExpense"],
                    data["incidentalRemarks"],
                    data["incidentalAmount"]
                )
            )
            self.__connection.commit()
            
        except mysql.connector.Error as e:
            print("[+] An error occurred while uploading the incidental details", e)
            db_lock.release()
            return False

        else:
            db_lock.release()
            return True
