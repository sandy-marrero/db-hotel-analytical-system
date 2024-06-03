"""LeastReserve Aggregate model for term project - hotel analytics system."""
from database.database import DatabaseConnection
from typing import Optional, Iterable
from config.config import DatabaseConfiguration

config = DatabaseConfiguration()


class LeastReserveDAO:
    """Data access object for LeastReserve aggregate."""

    def __init__(self):
        """Create LeastReserveDAO Object and connect to database.

        Connecting to database using config module
        Will raise an exception if it cannot connect to the database.
        """
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e

    def getLeastRooms(self, hid: int) -> Optional[Iterable]:
        """Get LeastReserve aggregate from database using hotel primary key.

        :param hid: Hotel table primary key
        :type hid: ``int``
        :rtype: ``Optional[Iterable]``
        """
        cursor = self.conn.conn.cursor()
        if self.conn.isHidInHotel(int(hid)) is False:
            return None
        query = """
        SELECT
        RID,
        HID,
        RDID,
        RPRICE,
        SUM(EXTRACT(DAY FROM ENDDATE::TIMESTAMP - STARTDATE::TIMESTAMP))
        AS TOTAL_DAYS_RESERVED
        FROM
        ROOMUNAVAILABLE
        NATURAL INNER JOIN ROOM
        WHERE
        HID = %s
        GROUP BY
        RID,
        HID,
        RDID,
        RPRICE
        ORDER BY
        TOTAL_DAYS_RESERVED
        LIMIT
        3;
        """
        cursor.execute(query, (hid, ))
        return cursor.fetchall()
