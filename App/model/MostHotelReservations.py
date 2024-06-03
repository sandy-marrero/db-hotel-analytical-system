from typing import Optional, Iterable
from database.database import DatabaseConnection
from config.config import DatabaseConfiguration
config = DatabaseConfiguration()
class MostHotelReservationsDAO:

    def __init__(self):
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e


    def getMostHotelReservations(self) -> Optional[Iterable]:
        cursor = self.conn.conn.cursor()
        query = """
        SELECT h.hname AS hotel_name, COUNT(re.reid) AS reservation_count
        FROM Hotel h
        JOIN Room r ON h.hid = r.hid
        JOIN RoomUnavailable ru ON r.rid = ru.rid
        JOIN Reserve re ON ru.ruid = re.ruid
        GROUP BY h.hname
        ORDER BY reservation_count DESC
        LIMIT (SELECT COUNT(*) * 0.10 FROM Reserve);
        """
        cursor.execute(query)
        return cursor.fetchall()
