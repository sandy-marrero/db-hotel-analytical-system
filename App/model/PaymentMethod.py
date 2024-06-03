from typing import Optional, Iterable
import psycopg2
from config.config import DatabaseConfiguration
from database.database import DatabaseConnection
config = DatabaseConfiguration()
class PaymentMethodDAO:

    def __init__(self):
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e


    def getPaymentMethod(self) -> Optional[Iterable]:
        cursor = self.conn.conn.cursor()
        query = """
        SELECT 
            payment AS payment_method,
            COUNT(*) AS count_payment,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reserve), 2) AS payment_percentage
        FROM 
            reserve
        GROUP BY 
            payment;

        """
        cursor.execute(query)
        return cursor.fetchall()
