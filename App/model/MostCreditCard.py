"""MostCreditCard Aggregate model for term project - hotel analytics system."""
from database.database import DatabaseConnection
from typing import Optional, Iterable
from config.config import DatabaseConfiguration

config = DatabaseConfiguration()


class MostCreditCardDAO:
    """Data access object for MostCreditCard aggregate."""

    def __init__(self):
        """Create MostCreditCardDAO Object and connect to database.

        Connecting to database using config module
        Will raise an exception if it cannot connect to the database.
        """
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e

    def getMostCreditCards(self, hid: int) -> Optional[Iterable]:
        """Get MostCreditCard aggregate from database using hotel primary key.

        :param hid: Hotel table primary key
        :type hid: ``int``
        :rtype: ``Optional[Iterable]``
        """
        cursor = self.conn.conn.cursor()
        if self.conn.isHidInHotel(int(hid)) is False:
            return None
        query = """
        SELECT
        CLID,
        FNAME,
        LNAME,
        AGE,
        MEMBERYEAR,
        COUNT(*) AS RESERVATION_COUNT
        FROM
        CLIENT
        NATURAL INNER JOIN HOTEL
        NATURAL INNER JOIN RESERVE
        NATURAL INNER JOIN ROOM
        NATURAL INNER JOIN ROOMUNAVAILABLE
        WHERE
        AGE < 30
        AND PAYMENT = 'credit card'
        AND HID = %s
        GROUP BY
        CLID,
        FNAME,
        LNAME,
        AGE,
        MEMBERYEAR
        ORDER BY
        RESERVATION_COUNT DESC
        LIMIT
        5;
        """
        cursor.execute(query, (hid, ))
        return cursor.fetchall()
