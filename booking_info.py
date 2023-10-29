from decimal import Decimal


class BookingInfo:
    def __init__(self, data_list: list):
        """
        Initialize BookingInfo with data from the database.

        Args:
            data_list (list): A list containing booking data (total_bookings, total_amount, timestamp).

        Note:
            The total_amount is converted to a Decimal type.

        """
        self.__total_bookings, self.__total_amount, self.__timestamp = data_list
        self.__total_amount = Decimal(self.__total_amount) if self.__total_amount else Decimal(0)

    def __str__(self) -> str:
        """
        Return a string representation of BookingInfo.

        Returns:
            str: A string in the format "Total Bookings: X, Total Amount: $Y".

        """
        return f"Total Bookings: {self.__total_bookings}, Total Amount: ${self.__total_amount}"

    def get_total_bookings(self) -> int:
        """
        Get the total number of bookings.

        Returns:
            int: The total number of bookings.

        """
        return self.__total_bookings

    def get_total_amount(self) -> Decimal:
        """
        Get the total booking amount as a Decimal.

        Returns:
            Decimal: The total booking amount.

        """
        return self.__total_amount

    def get_timestamp(self) -> str:
        """
        Get the timestamp associated with the booking data.

        Returns:
            str: The timestamp as a string.

        """
        return self.__timestamp
