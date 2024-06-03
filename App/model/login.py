from typing import List, Tuple
from database.database import DatabaseConnection
from config.config import DatabaseConfiguration
config = DatabaseConfiguration()
class LoginDAO:
    def __init__(self):
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e
    def getAll(self) -> List[Tuple[int, int, str, str]]:
        cursor = self.conn.conn.cursor()
        cursor.execute("SELECT * FROM Login")
        logins = cursor.fetchall()
        return logins
    
    def getById(self, id) -> Tuple[int, int, str, str]:
        cursor = self.conn.conn.cursor()
        cursor.execute(f"SELECT * FROM Login WHERE lid = {id}")
        login = cursor.fetchone()
        return login
    
    def update_login(self, id, eid, user, password):
        cursor = self.conn.conn.cursor()
        try:
            cursor.execute("SELECT eid from login where lid = %s", (id,))
            self.conn.conn.commit()
            loginEid = cursor.fetchone()[0]
            if self.conn.isEidInLogin(eid) is True and eid != loginEid:
                return False
            cursor.execute(f"UPDATE Login SET eid = {eid}, username = '{user}', password = '{password}' WHERE lid = {id} returning lid")
            self.conn.conn.commit()
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                return int(result[0])
        except Exception:
            return None
    
    def create_login(self, eid, user, password):
        cursor = self.conn.conn.cursor()
        if self.conn.isEidInLogin(eid) is True:
            return False
        cursor.execute(f"INSERT INTO Login (eid, username, password) VALUES ({eid}, '{user}', '{password}') returning lid")
        self.conn.conn.commit()
        id = int(cursor.fetchone()[0])
        return id
        
    def delete_login(self, id):
        if self.conn.isLidInLogin(id) is False:
            return False
        cursor = self.conn.conn.cursor()
        query = f"DELETE FROM Login WHERE lid = {id}"
        try:
            cursor.execute(query)
            self.conn.conn.commit()
            return True
        except Exception:
            return False