from typing import Optional, Iterable
from database.database import DatabaseConnection
from config.config import DatabaseConfiguration
config = DatabaseConfiguration()
class LeastRoomsDAO:

    def __init__(self):
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e


    def getLeastRooms(self) -> Optional[Iterable]:
        cursor = self.conn.conn.cursor()
        query = """
        SELECT c.cname, COUNT(r.rid) AS num_rooms
        FROM chains c
        JOIN hotel h ON c.chid = h.chid
        JOIN room r ON h.hid= r.hid
        GROUP BY c.chid, c.chid
        ORDER BY num_rooms
        LIMIT 3;
        """
        cursor.execute(query)
        return cursor.fetchall()
