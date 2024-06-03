"""HandicapRoom Aggregate model for term project - hotel analytics system."""
from database.database import DatabaseConnection
from typing import Optional, Iterable
from config.config import DatabaseConfiguration

config = DatabaseConfiguration()


class HandicapRoomDAO:
    """Data access object for HandicapRoom aggregate."""

    def __init__(self):
        """Create HandicapRoomDAO Object and connect to database.

        Connecting to database using config module
        Will raise an exception if it cannot connect to the database.
        """
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e

    def getHandicapRoomReserveCountDAO(self, hid: int) -> Optional[Iterable]:
        """Get HandicapRoom aggregate from database using hotel primary key.

        :param hid: Hotel table primary key
        :type hid: ``int``
        :rtype: ``Optional[Iterable]``
        """
        cursor = self.conn.conn.cursor()
        if self.conn.isHidInHotel(int(hid)) is False:
            return None
        query = """SELECT RID, HID, RDID, RPRICE, COUNT(*) FROM ROOM
        NATURAL INNER JOIN ROOMDESCRIPTION
        NATURAL INNER JOIN RESERVE
        NATURAL INNER JOIN ROOMUNAVAILABLE
        WHERE ISHANDICAP = TRUE AND HID = %s
        GROUP BY RID ORDER BY COUNT(*) DESC LIMIT 5;"""
        cursor.execute(query, (hid, ))
        return cursor.fetchall()
