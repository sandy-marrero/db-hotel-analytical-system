"""HighestPaid Aggregate model for term project - hotel analytics system."""
from database.database import DatabaseConnection
from typing import Optional, Iterable
from config.config import DatabaseConfiguration

config = DatabaseConfiguration()


class HighestPaidDAO:
    """Data access object for HighestPaid aggregate."""

    def __init__(self):
        """Create HighestPaidDAO Object and connect to database.

        Connecting to database using config module
        Will raise an exception if it cannot connect to the database.
        """
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e

    def getHighestPaid(self, hid: int) -> Optional[Iterable]:
        """Get HighestPaid aggregate from database using hotel primary key.

        :param hid: Hotel table primary key
        :type hid: ``int``
        :rtype: ``Optional[Iterable]``
        """
        cursor = self.conn.conn.cursor()
        if self.conn.isHidInHotel(int(hid)) is False:
            return None
        query = """
        SELECT
        EID,
        HID,
        FNAME,
        LNAME,
        AGE,
        SALARY
        FROM
        EMPLOYEE
        WHERE
        HID = %s
        ORDER BY
        SALARY DESC
        LIMIT
        3;
        """
        cursor.execute(query, (hid, ))
        return cursor.fetchall()
