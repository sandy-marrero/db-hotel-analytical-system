from typing import Optional, Iterable
import psycopg2
from config.config import DatabaseConfiguration
from database.database import DatabaseConnection
config = DatabaseConfiguration()
class MostRevenueDAO:

    def __init__(self):
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                        config.DB_PASS, config.DB_HOST,
                                        config.DB_PORT)
        except Exception as e:
            raise e

    
    def getMostRevenue(self) -> Optional[Iterable]:
        cursor = self.conn.conn.cursor()
        query = """
        SELECT
            c.cname AS chain_name,
            SUM(r.total_cost
            ) AS total_revenue
        FROM
            Reserve r
        JOIN
            RoomUnavailable ru ON r.ruid = ru.ruid
        JOIN
            Room rm ON ru.rid = rm.rid
        JOIN
            Hotel h ON rm.hid = h.hid
        JOIN
            Chains c ON h.chid = c.chid
        GROUP BY
            c.cname
        ORDER BY
            total_revenue DESC
        LIMIT 3;
        """
        cursor.execute(query)
        return cursor.fetchall()
