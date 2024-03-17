import threading
from os import environ

import mysql.connector
from dotenv import load_dotenv

from logging_module import logger

# Creating the lock for the database
db_lock = threading.RLock()


class Database:
    """
    The database class to connect to the database
    """

    def __init__(self):
        print("Database connecting...")
        logger.info("Database connecting...")

        try:
            self.__connection = mysql.connector.connect(
                host=environ.get("DB_HOST"),
                user=environ.get("DB_USER"),
                password=environ.get("DB_PASSWORD"),
                database=environ.get("DB_DATABASE"),
                autocommit=True,
                use_pure=True,
            )
            self.__cursor = self.__connection.cursor()
            print("Connected to the database")
            logger.info("Connected to the database")

        except Exception as e:
            self.__connection = None
            print("An error occurred", type(e).__name__, e)
            logger.critical(f"An error occurred {type(e).__name__} {e}")

    def is_db_connected(self):
        if self.__connection is not None:
            return True
        print("Database is not connected")
        logger.error("Database is not connected")
        return False

    def disconnect(self):
        if self.__connection is not None:
            self.__connection.close()
            self.__cursor.close()

            print("Disconnected from the database")
            logger.info("Disconnected from the database")

    def upload_the_travel(self, data: dict):
        """
        Upload the travel details in the travel table
        """

        db_lock.acquire()

        try:
            self.__cursor.execute(
                "INSERT INTO travel VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data["travelId"],
                    data["empId"],
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
                    0,
                    0,
                ),
            )
            self.__connection.commit()

        except mysql.connector.Error as e:
            print("An error occurred while uploading the travel details", e)
            logger.warning(
                f"An error occurred while uploading the travel details {e}")

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
                "INSERT INTO conveyance VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data["conveyanceId"],
                    data["travelId"],
                    data["conveyanceDate"],
                    data["conveyanceFrom"],
                    data["conveyanceTo"],
                    data["conveyanceMode"],
                    data["conveyancePurpose"],
                    data["conveyanceAmount"],
                ),
            )
            self.__connection.commit()

        except mysql.connector.Error as e:
            print("An error occurred while uploading the conveyance details", e)
            logger.warning(
                f"An error occurred while uploading the conveyance details {e}")

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
                "INSERT INTO food_lodging VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    data["foodLodgingId"],
                    data["travelId"],
                    data["foodLodgingDate"],
                    data["foodLodgingBillNo"],
                    data["foodLodgingHotel"],
                    data["foodLodgingOccupancy"],
                    data["foodLodgingAmount"],
                ),
            )
            self.__connection.commit()

        except mysql.connector.Error as e:
            print("An error occurred while uploading the food and lodging details", e)
            logger.warning(
                f"An error occurred while uploading the food and lodging details {e}")

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
                "INSERT INTO incidental VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    data["incidentalId"],
                    data["travelId"],
                    data["incidentalDate"],
                    data["incidentalExpense"],
                    data["incidentalRemarks"],
                    data["incidentalAmount"],
                ),
            )
            self.__connection.commit()

        except mysql.connector.Error as e:
            print("An error occurred while uploading the incidental details", e)
            logger.warning(
                f"An error occurred while uploading the incidental details {e}")

            db_lock.release()
            return False

        else:
            db_lock.release()
            return True

    def get_all_bill_from_travel_id(self, travel_id: str):
        """
        Get all the bill ids from the travel id
        """
        all_bills = []  # [(bill_id, amount), (bill_id, amount), ...)]

        db_lock.acquire()

        try:
            self.__cursor.execute(
                "SELECT conveyanceId, conveyanceAmount FROM conveyance WHERE travelId = %s", (travel_id,))
            all_bills.extend(self.__cursor.fetchall())

            self.__cursor.execute(
                "SELECT foodLodgingId, foodLodgingAmount FROM food_lodging WHERE travelId = %s", (travel_id,))
            all_bills.extend(self.__cursor.fetchall())

            self.__cursor.execute(
                "SELECT incidentalId, incidentalAmount FROM incidental WHERE travelId = %s", (travel_id,))
            all_bills.extend(self.__cursor.fetchall())

        except mysql.connector.Error as e:
            print("An error occurred while getting the bill ids", e)
            logger.warning(f"An error occurred while getting the bill ids {e}")

            db_lock.release()
            return None

        else:
            db_lock.release()
            return all_bills


if __name__ == "__main__":
    db = Database()
    db.disconnect()
