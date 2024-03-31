from os import environ
from threading import RLock

from sqlalchemy import create_engine, exc, text

from modules.logging_module import logger

# Creating the lock for the database
db_lock = RLock()

# Importing all environment variables
DATABASE_URI = (
    f"mysql://{environ.get('DB_USER')}:{environ.get('DB_PASSWORD')}@{environ.get('DB_HOST')}:{environ.get('DB_PORT')}/{environ.get('DB_DATABASE')}"
)


class Database:
    """
    The database class to connect to the database
    """

    def __init__(self):
        print("Database connecting...")
        logger.info("Database connecting...")

        try:
            self.__engine = create_engine(
                DATABASE_URI,
                pool_size=2,
                max_overflow=5,
                pool_timeout=30,
                pool_recycle=3600,
                pool_pre_ping=True,
                # echo=True,
                future=True,
                connect_args={"autocommit": True},
            )

            # Database pool warmup successfully
            for _ in range(self.__engine.pool.size()):
                conn = self.__engine.connect()
                conn.close()

            print("Connected to the database")
            logger.info("Connected to the database")

        except exc.SQLAlchemyError as error_name:
            self.__engine = ""
            print("Error", error_name)
            logger.critical(f"An error occurred {error_name}")

    def is_db_connected(self):
        return bool(self.__engine)

    def upload_the_travel(self, data: dict):
        """
        Upload the travel details in the travel table
        """

        db_lock.acquire()

        try:
            with self.__engine.connect() as conn:
                conn.execute(
                    text(
                        "INSERT INTO travel VALUES (:travelId, :empId, :travelDate, :travelFrom, :travelTo, :travelMode, :travelClass, :travelFare, :travelConveyance, :travelFoodLodging, :travelIncidental, :travelTotal, 0, 0)"
                    ),
                    {
                        "travelId": data["travelId"],
                        "empId": data["empId"],
                        "travelDate": data["travelDate"],
                        "travelFrom": data["travelFrom"],
                        "travelTo": data["travelTo"],
                        "travelMode": data["travelMode"],
                        "travelClass": data["travelClass"],
                        "travelFare": data["travelFare"],
                        "travelConveyance": data["travelConveyance"],
                        "travelFoodLodging": data["travelFoodLodging"],
                        "travelIncidental": data["travelIncidental"],
                        "travelTotal": data["travelTotal"],
                    },
                )

        except exc.SQLAlchemyError as e:
            print("An error occurred while uploading the travel details", e)
            logger.warning(f"An error occurred while uploading the travel details {e}")

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
            with self.__engine.connect() as conn:
                conn.execute(
                    text(
                        "INSERT INTO conveyance VALUES (:conveyanceId, :travelId, :conveyanceDate, :conveyanceFrom, :conveyanceTo, :conveyanceMode, :conveyancePurpose, :conveyanceAmount)"
                    ),
                    {
                        "conveyanceId": data["conveyanceId"],
                        "travelId": data["travelId"],
                        "conveyanceDate": data["conveyanceDate"],
                        "conveyanceFrom": data["conveyanceFrom"],
                        "conveyanceTo": data["conveyanceTo"],
                        "conveyanceMode": data["conveyanceMode"],
                        "conveyancePurpose": data["conveyancePurpose"],
                        "conveyanceAmount": data["conveyanceAmount"],
                    },
                )

        except exc.SQLAlchemyError as e:
            print("An error occurred while uploading the conveyance details", e)
            logger.warning(f"An error occurred while uploading the conveyance details {e}")

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
            with self.__engine.connect() as conn:
                conn.execute(
                    text(
                        "INSERT INTO food_lodging VALUES (:foodLodgingId, :travelId, :foodLodgingDate, :foodLodgingBillNo, :foodLodgingHotel, :foodLodgingOccupancy, :foodLodgingAmount)"
                    ),
                    {
                        "foodLodgingId": data["foodLodgingId"],
                        "travelId": data["travelId"],
                        "foodLodgingDate": data["foodLodgingDate"],
                        "foodLodgingBillNo": data["foodLodgingBillNo"],
                        "foodLodgingHotel": data["foodLodgingHotel"],
                        "foodLodgingOccupancy": data["foodLodgingOccupancy"],
                        "foodLodgingAmount": data["foodLodgingAmount"],
                    },
                )

        except exc.SQLAlchemyError as e:
            print("An error occurred while uploading the food and lodging details", e)
            logger.warning(f"An error occurred while uploading the food and lodging details {e}")

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
            with self.__engine.connect() as conn:
                conn.execute(
                    text(
                        "INSERT INTO incidental VALUES (:incidentalId, :travelId, :incidentalDate, :incidentalExpense, :incidentalRemarks, :incidentalAmount)"
                    ),
                    {
                        "incidentalId": data["incidentalId"],
                        "travelId": data["travelId"],
                        "incidentalDate": data["incidentalDate"],
                        "incidentalExpense": data["incidentalExpense"],
                        "incidentalRemarks": data["incidentalRemarks"],
                        "incidentalAmount": data["incidentalAmount"],
                    },
                )

        except exc.SQLAlchemyError as e:
            print("An error occurred while uploading the incidental details", e)
            logger.warning(f"An error occurred while uploading the incidental details {e}")

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
            self.__cursor.execute("SELECT conveyanceId, conveyanceAmount FROM conveyance WHERE travelId = %s", (travel_id,))
            all_bills.extend(self.__cursor.fetchall())

            self.__cursor.execute("SELECT foodLodgingId, foodLodgingAmount FROM food_lodging WHERE travelId = %s", (travel_id,))
            all_bills.extend(self.__cursor.fetchall())

            self.__cursor.execute("SELECT incidentalId, incidentalAmount FROM incidental WHERE travelId = %s", (travel_id,))
            all_bills.extend(self.__cursor.fetchall())

        except mysql.connector.Error as e:
            print("An error occurred while getting the bill ids", e)
            logger.warning(f"An error occurred while getting the bill ids {e}")

            db_lock.release()
            return None

        else:
            db_lock.release()
            return all_bills
