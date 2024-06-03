from database.database import DatabaseConnection
from typing import Optional, Iterable
from config.config import DatabaseConfiguration

config = DatabaseConfiguration()

class MostDiscountDAO:

    def __init__(self):
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e

    def getMostDiscountDAO(self, clid: int) -> Optional[Iterable]:
        cursor = self.conn.conn.cursor()
        if self.conn.isClidInClient(int(clid)) is False:
            return None
        
#       The reservation cost is calculated by using the room priced times the number of days reserved
#       times the season markup of the hotel’s chain less the membership discount.

        query = """SELECT CLID, CONCAT(FNAME, ' ', LNAME) AS FULL_NAME, ROUND(
        (ROOM.RPRICE::DECIMAL * (ROOMUNAVAILABLE.ENDDATE - ROOMUNAVAILABLE.STARTDATE) * 
        (CASE
            WHEN EXTRACT(MONTH FROM ROOMUNAVAILABLE.STARTDATE) BETWEEN 3 AND 5 THEN CHAINS.SPRINGMKUP
            WHEN EXTRACT(MONTH FROM ROOMUNAVAILABLE.STARTDATE) BETWEEN 6 AND 8 THEN CHAINS.SUMMERMKUP
            WHEN EXTRACT(MONTH FROM ROOMUNAVAILABLE.STARTDATE) BETWEEN 9 AND 11 THEN CHAINS.FALLMKUP
            ELSE CHAINS.WINTERMKUP
        END) -
        (ROOM.RPRICE * (ROOMUNAVAILABLE.ENDDATE - ROOMUNAVAILABLE.STARTDATE) * 
        (CASE
            WHEN EXTRACT(MONTH FROM ROOMUNAVAILABLE.STARTDATE) BETWEEN 3 AND 5 THEN CHAINS.SPRINGMKUP
            WHEN EXTRACT(MONTH FROM ROOMUNAVAILABLE.STARTDATE) BETWEEN 6 AND 8 THEN CHAINS.SUMMERMKUP
            WHEN EXTRACT(MONTH FROM ROOMUNAVAILABLE.STARTDATE) BETWEEN 9 AND 11 THEN CHAINS.FALLMKUP
            ELSE CHAINS.WINTERMKUP
        END) * 
        (1 - CASE
            WHEN MEMBERYEAR BETWEEN 1 AND  4 THEN 0.02
            WHEN MEMBERYEAR BETWEEN 5 AND  9 THEN 0.05
            WHEN MEMBERYEAR BETWEEN 10 AND 14 THEN 0.08
            WHEN MEMBERYEAR > 15 THEN 0.12
            ELSE 0 
        END)))::DECIMAL
        ,2) AS DISCOUNT
        
        FROM CLIENT
        NATURAL INNER JOIN ROOMUNAVAILABLE
        NATURAL INNER JOIN CHAINS
        NATURAL INNER JOIN ROOM
        NATURAL INNER JOIN RESERVE
        NATURAL INNER JOIN HOTEL
        WHERE hotel.hid = %s
        GROUP BY CLID, FULL_NAME, MEMBERYEAR, ROOM.RPRICE, ROOMUNAVAILABLE.ENDDATE, ROOMUNAVAILABLE.STARTDATE,
        CHAINS.SPRINGMKUP, CHAINS.SUMMERMKUP, CHAINS.FALLMKUP, CHAINS.WINTERMKUP, RESERVE.TOTAL_COST
        ORDER BY DISCOUNT DESC 
        LIMIT 5;
        """
        
        cursor.execute(query, (clid, ))
        return cursor.fetchall()