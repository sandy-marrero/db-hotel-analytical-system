from database.database import DatabaseConnection
from typing import Optional, Iterable
from config.config import DatabaseConfiguration

config = DatabaseConfiguration()

class LeastGuestsDAO:

    def __init__(self):
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e

    def getLeastGuestsDAO(self, reid: int) -> Optional[Iterable]:
        cursor = self.conn.conn.cursor()
        if self.conn.isReidInReserve(int(reid)) is False:
            return None
        
        query = """SELECT ROOM.RID AS RID, ROUND(AVG(RESERVE.GUESTS::DECIMAL / ROOMDESCRIPTION.capacity),2) AS GUEST_TO_CAP_RATIO
            FROM ROOM
            NATURAL INNER JOIN RESERVE 
            NATURAL INNER JOIN ROOMDESCRIPTION
            NATURAL INNER JOIN ROOMUNAVAILABLE
            NATURAL INNER JOIN HOTEL
            WHERE HID = %s
            GROUP BY RID
            ORDER BY GUEST_TO_CAP_RATIO ASC LIMIT 3;"""
        
        cursor.execute(query, (reid, ))
        return cursor.fetchall()