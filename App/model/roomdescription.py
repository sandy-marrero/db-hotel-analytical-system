from typing import List, Tuple
import psycopg2
from database.database import DatabaseConnection
from config.config import DatabaseConfiguration
config = DatabaseConfiguration()
class RoomDescriptionDAO:

    def __init__(self) -> None:
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e
            
    def getAll(self) -> List[Tuple[int, str, str, int, bool]]:
        cursor = self.conn.conn.cursor()
        cursor.execute("SELECT * FROM RoomDescription")
        roomDescriptions = cursor.fetchall()
        return roomDescriptions
    
    def getById(self, id) -> Tuple[int, str, str, int, bool]:
        cursor = self.conn.conn.cursor()
        cursor.execute(f"SELECT * FROM RoomDescription WHERE rdid = {id}")
        roomDescription = cursor.fetchone()
        return roomDescription
    
    def update_roomDescription(self, id: int, rname: str, rtype: str, capacity: int, ishandicap: bool) -> (str, int):
        cursor = self.conn.conn.cursor()
        try:
            cursor.execute(f"""UPDATE RoomDescription SET rname = '{rname}', 
                                                        rtype = '{rtype}',
                                                        capacity = '{capacity}',
                                                        ishandicap = '{ishandicap}'
                                                        WHERE rdid = {id}
                                                        returning rdid""")
            self.conn.conn.commit()
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                return int(result[0])
        except Exception:
            return None
    
    def create_roomDescription(self, rname: str, rtype: str, capacity: int, ishandicap: bool) -> int:
        cursor = self.conn.conn.cursor()
        query = """INSERT INTO RoomDescription (rname, rtype, capacity, ishandicap)
                    VALUES (%s, %s, %s, %s) returning rdid"""
        try:
            cursor.execute(query, (rname, rtype, capacity, ishandicap))
            self.conn.conn.commit()
            roomDescription_id = cursor.fetchone()[0]
            return roomDescription_id
        except Exception:
            return None

    
    def delete_roomRescription(self, rdid: int) -> bool:
        if self.conn.isRdidInRoomDescription(rdid) is False:
            return False
        cursor = self.conn.conn.cursor()
        query = """DELETE from RoomDescription where rdid = %s"""
        try:
            cursor.execute(query, (rdid, ))
            self.conn.conn.commit()
            return True
        except Exception:
            return False
