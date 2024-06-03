from typing import Optional, Iterable
from database.database import DatabaseConnection
from config.config import DatabaseConfiguration
config = DatabaseConfiguration()
class MostChainReservationsDAO:

    def __init__(self):
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e


    def getMostChainReservations(self) -> Optional[Iterable]:
        cursor = self.conn.conn.cursor()
        query = """
        WITH RankedReservations AS (
            SELECT 
                c.cname AS chain_name, 
                EXTRACT(MONTH FROM ru.startdate) AS reservation_month, 
                COUNT(re.reid) AS reservation_count,
                ROW_NUMBER() OVER (PARTITION BY c.cname ORDER BY COUNT(re.reid) DESC) AS rank
            FROM Chains c
            JOIN Hotel h ON c.chid = h.chid
            JOIN Room r ON h.hid = r.hid
            JOIN RoomUnavailable ru ON r.rid = ru.rid
            JOIN Reserve re ON ru.ruid = re.ruid
            GROUP BY c.cname, reservation_month
        )
        SELECT chain_name, reservation_month, reservation_count
        FROM RankedReservations
        WHERE rank <= 3
        ORDER BY chain_name, reservation_count DESC;
        """
        cursor.execute(query)
        return cursor.fetchall()
