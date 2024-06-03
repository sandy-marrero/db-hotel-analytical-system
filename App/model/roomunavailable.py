from typing import List, Tuple
import psycopg2
from config.config import DatabaseConfiguration
from database.database import DatabaseConnection

# should i use a date data type or use
from datetime import date


class RoomUnavailableDAO:
    def __init__(self) -> None:
        self.conn = DatabaseConnection(
            DB_HOST= DatabaseConfiguration.DB_HOST,
            DB_NAME=DatabaseConfiguration.DB_NAME,
            DB_USER=DatabaseConfiguration.DB_USER,
            DB_PASS=DatabaseConfiguration.DB_PASS,
            DB_PORT=DatabaseConfiguration.DB_PORT
        )
    
    def validateRoomUnavailableEntry(self, ruid, rid) -> bool:
        return self.conn.isRuidInRoomUnavailable(ruid) and \
            self.conn.isRidInRoomUnavailable(rid)
    
    def getAll(self) -> List[Tuple[int, int, date, date]]:
        cursor = self.conn.conn.cursor()
        cursor.execute("SELECT * FROM RoomUnavailable")
        roomunavailable = cursor.fetchall()
        return roomunavailable

    def getById(self, id) -> Tuple[int, int, date, date]:
        cursor = self.conn.conn.cursor()
        cursor.execute(f"SELECT * FROM RoomUnavailable WHERE ruid = {id}")
        roomunavailable = cursor.fetchone()
        return roomunavailable
    

    def addRoomUnavailable(self, rid:int, startdate: date, enddate: date) -> int:
        if self.conn.isRidInRoom(rid) == False:
            return False
        if self.conn.isReservationConflict(rid, startdate, enddate) == False:
            return False
        cursor = self.conn.conn.cursor()
        cursor.execute("INSERT INTO RoomUnavailable (rid, startdate, enddate) VALUES (%s, %s, %s) RETURNING ruid",
                       (rid, startdate, enddate))
        roomunavailable_id = cursor.fetchone()[0]
        self.conn.conn.commit()
        return roomunavailable_id

    def updateRoomUnavailable(self, id: int, rid: int, startdate: date, enddate: date) -> None:
        if self.validateRoomUnavailableEntry(id, rid) is False:
            return False
        if self.conn.isReservationConflict(rid, startdate, enddate) == False:
            return False
        cursor = self.conn.conn.cursor()
        cursor.execute("UPDATE RoomUnavailable SET rid = %s, startdate = %s, enddate = %s WHERE ruid = %s",
                       (rid, startdate, enddate, id))
        self.conn.conn.commit()
        return id

    def deleteRoomUnavailable(self, ruid: int) -> bool:
        if self.conn.isRuidInRoomUnavailable(ruid) is False:
            return False
        cursor = self.conn.conn.cursor()
        query = """DELETE from roomunavailable where ruid = %s"""
        try:
            cursor.execute(query, (ruid, ))
            self.conn.conn.commit()
            return True
        except Exception:
            return False
    
