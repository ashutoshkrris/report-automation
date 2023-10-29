from datetime import datetime
import psycopg2
import logging
import os
import pandas as pd

from booking_info import BookingInfo


logging.basicConfig(
    format="%(asctime)s | %(levelname)s : %(message)s", level=logging.INFO
)

DB_CONFIG = {
    "host": os.environ.get("DB_HOSTNAME"),
    "database": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USERNAME"),
    "password": os.environ.get("DB_PASSWORD"),
}


class DataExporter:
    def __init__(self):
        """Initialize the DataExporter with the database configuration."""
        self.db_config = DB_CONFIG

    def __connect_to_database(self) -> None:
        """
        Establish a connection to the PostgreSQL database.

        Raises:
            Exception: If a connection to the database cannot be established.
        """
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            logging.info("Connected to the database")
        except Exception as e:
            logging.error(
                "Failed to connect to the database with error: %s", e)
            raise

    def __fetch_from_database(self, start_timestamp, end_timestamp) -> tuple | None:
        """
        Fetch booking data from the database for a given time range.

        Args:
            start_timestamp (datetime): The start of the time range.
            end_timestamp (datetime): The end of the time range.

        Returns:
            list: A list containing booking data (num_bookings, total_amount) or None if an error occurs.
        """
        self.__connect_to_database()
        query = f"""
        SELECT COUNT(*) AS num_bookings, SUM(total_amount) AS total_amount
        FROM bookings
        WHERE book_date >= {int(start_timestamp.timestamp()) * 1000} AND book_date <= {int(end_timestamp.timestamp()) * 1000}
        """
        logging.info(
            "Exracting bookings data from database for start timestamp=%s and end_timestamp=%s",
            start_timestamp,
            end_timestamp,
        )
        result = None
        try:
            self.cursor.execute(query)
            result = list(self.cursor.fetchone())
            result.append(
                f'{start_timestamp.strftime("%d %b, %Y")} - {end_timestamp.strftime("%d %b, %Y")}'
            )
            logging.info(
                "Successfully exracted bookings data from database for start timestamp=%s and end_timestamp=%s",
                start_timestamp,
                end_timestamp,
            )
        except Exception as e:
            logging.error(
                "Error occurred while extracting bookings data from database: %s", e
            )
        return result

    def __convert_to_excelsheet(self, data: list, sheet_name: str):
        """
        Convert the fetched data into an Excel sheet.

        Args:
            data (list): A list containing booking data.
            sheet_name (str): Name of the Excel sheet to be created.

        Raises:
            ValueError: If there is an error in converting data to an Excel sheet.
        """
        try:
            booking_info = BookingInfo(data)
            data = {
                "": ["Total Bookings", "Total Amount ($)"],
                booking_info.get_timestamp(): [
                    booking_info.get_total_bookings(),
                    booking_info.get_total_amount(),
                ],
            }
            logging.info("Converting the data into pandas dataframe")
            df = pd.DataFrame(data)
            logging.info("Inserting the data into the excelsheet")
            with pd.ExcelWriter(sheet_name, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="Sheet1", index=False)
            logging.info("Successfully inserted data into the excelsheet")
        except ValueError as e:
            logging.error("Error converting data into excel: %s", e)

    def generate_excelsheet(
        self,
        start_timestamp: datetime,
        end_timestamp: datetime,
        sheet_name: str = "Bookings Data.xlsx",
    ) -> bool:
        """
        Generate an Excel sheet with booking data for a specified time range.

        Args:
            start_timestamp (datetime): The start of the time range.
            end_timestamp (datetime): The end of the time range.
            sheet_name (str, optional): Name of the Excel sheet to be created. Defaults to "Bookings Data.xlsx".

        Returns:
            bool: True if excelsheet was generated successfully else False

        Note:
            This method logs errors but does not raise exceptions to avoid breaking the workflow.
        """
        data = self.__fetch_from_database(start_timestamp, end_timestamp)
        if data is not None:
            self.__convert_to_excelsheet(data, sheet_name)
            return True
        else:
            logging.error("No data to convert generate excelsheet")
            return False
