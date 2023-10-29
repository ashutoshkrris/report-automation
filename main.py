from exporter import DataExporter
from datetime import datetime
from mailer import send_email

start_timestamp = datetime(2023, 5, 28, 00, 00, 00)  # May 28 2023 00:00:00
end_timestamp = datetime(2023, 8, 20, 23, 59, 59)  # Aug 20 2023 23:59:59

exporter = DataExporter()
if exporter.generate_excelsheet(
        start_timestamp, end_timestamp, sheet_name="Bookings Data.xlsx"):
    send_email("myemail@gmail.com", "Your Report", "Bookings Data.xlsx")
