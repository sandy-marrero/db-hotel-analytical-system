from typing import Optional, Iterable
from database.database import DatabaseConnection
from config.config import DatabaseConfiguration
config = DatabaseConfiguration()
class MostClientCapacityDAO:

    def __init__(self):
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e


    def getMostClientCapacity(self) -> Optional[Iterable]:
        cursor = self.conn.conn.cursor()
        query = """
        SELECT h.hname AS hotel_name, SUM(rd.capacity) AS total_capacity
        FROM Hotel h
        JOIN Room r ON h.hid = r.hid
        JOIN RoomDescription rd ON r.rdid = rd.rdid
        GROUP BY h.hname
        ORDER BY total_capacity DESC
        LIMIT 5;
        """
        cursor.execute(query)
        return cursor.fetchall()
