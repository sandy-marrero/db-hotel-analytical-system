from database.database import DatabaseConnection
from typing import Optional, Iterable
from config.config import DatabaseConfiguration

config = DatabaseConfiguration()

class RoomTypeDAO:

    def __init__(self):
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e

    def getRoomTypeDAO(self, ruid: int) -> Optional[Iterable]:
        cursor = self.conn.conn.cursor()
        if self.conn.isRuidInRoomUnavailable(int(ruid)) is False:
            return None
        
        query = """SELECT ROOMDESCRIPTION.RTYPE AS RTYPE, COUNT(*)
        FROM ROOMDESCRIPTION
        NATURAL INNER JOIN RESERVE
        NATURAL INNER JOIN ROOMUNAVAILABLE
        NATURAL INNER JOIN ROOM
        WHERE HID = %s
        GROUP BY RTYPE 
        ORDER BY COUNT(*) DESC;"""
        
        cursor.execute(query, (ruid, ))
        return cursor.fetchall()