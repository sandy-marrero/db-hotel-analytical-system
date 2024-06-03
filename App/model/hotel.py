from typing import List, Tuple
import psycopg2
from config.config import DatabaseConfiguration
from database.database import DatabaseConnection


class HotelDAO:
    def __init__(self) -> None:
        self.conn = DatabaseConnection(
                DB_HOST= DatabaseConfiguration.DB_HOST,
                DB_NAME=DatabaseConfiguration.DB_NAME,
                DB_USER=DatabaseConfiguration.DB_USER,
                DB_PASS=DatabaseConfiguration.DB_PASS,
                DB_PORT=DatabaseConfiguration.DB_PORT
            )
    
    def validateHotelEntry(self, hid, chid) -> bool:
        return self.conn.isHidInHotel(hid) and \
            self.conn.isChidInHotel(chid)
    
    def getAll(self) -> List[Tuple[int, int, str, str]]:
        cursor = self.conn.conn.cursor()
        cursor.execute("SELECT * FROM Hotel")
        hotel = cursor.fetchall()
        return hotel

    def getById(self, id) -> Tuple[int, int, str, str]:
        cursor = self.conn.conn.cursor()
        cursor.execute(f"SELECT * FROM Hotel WHERE hid = {id}")
        hotel = cursor.fetchone()
        return hotel
    
    def addHotel(self, chid: int, hname: str, hcity: str) -> int:
        if self.conn.isChidInHotel(chid) == False:
            return False
        cursor = self.conn.conn.cursor()
        cursor.execute("INSERT INTO Hotel (chid, hname, hcity) VALUES (%s, %s, %s) RETURNING hid",
                       (chid,hname, hcity))
        self.conn.conn.commit()
        hotel_id = cursor.fetchone()[0]
        return hotel_id
    
    def updateHotel(self, id: int, chid: int, hname: str, hcity: str) -> None:
        if self.validateHotelEntry(id, chid) is False:
            return False
        cursor = self.conn.conn.cursor()
        cursor.execute("UPDATE Hotel SET chid = %s,hname = %s, hcity = %s WHERE hid = %s",
                       (chid, hname, hcity, id))
        self.conn.conn.commit()
        return id

    def deleteHotel(self, hid: int) -> bool:
        if self.conn.isHidInHotel(hid) is False:
            return False
        cursor = self.conn.conn.cursor()
        query = """DELETE from hotel where hid = %s"""
        try:
            cursor.execute(query, (hid, ))
            self.conn.conn.commit()
            return True
        except Exception:
            return False
    