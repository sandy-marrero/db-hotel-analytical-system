from typing import List, Tuple
from typing import List, Tuple
from config.config import DatabaseConfiguration
from database.database import DatabaseConnection
config = DatabaseConfiguration()
class ChainsDAO:
    def __init__(self):
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e
    def getAll(self) -> List[Tuple[int, str, int, int, int, int]]:
        cursor = self.conn.conn.cursor()
        cursor.execute("SELECT * FROM Chains")
        chains = cursor.fetchall()
        return chains

    def getById(self, id) -> Tuple[int, str, int, int, int, int]:
        cursor = self.conn.conn.cursor()
        cursor.execute(f"SELECT * FROM Chains WHERE chid = {id}")
        chain = cursor.fetchone()
        return chain
    
    def addChain(self, cname: str, springmkup: int, summermkup: int, fallmkup: int, wintermkup: int) -> int:
        cursor = self.conn.conn.cursor()
        cursor.execute("INSERT INTO Chains (cname, springmkup, summermkup, fallmkup, wintermkup) VALUES (%s, %s, %s, %s, %s) RETURNING chid",
                       (cname, springmkup, summermkup, fallmkup, wintermkup))
        chain_id = cursor.fetchone()[0]
        self.conn.conn.commit()
        return chain_id

    def updateChain(self, id: int, name: str, springmkup: int, summermkup: int, fallmkup: int, wintermkup: int) -> (str,int):
        cursor = self.conn.conn.cursor()
        try:
            cursor.execute("UPDATE Chains SET cname = %s, springmkup = %s, summermkup = %s, fallmkup = %s, wintermkup = %s WHERE chid = %s returning chid",
                       (name, springmkup, summermkup, fallmkup, wintermkup, id))
            self.conn.conn.commit()
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                return int(result[0])
        except Exception:
            return None

    def deleteChain(self, chid: int) -> None:
        if self.conn.isChidInChains(chid) is False:
            return False
        cursor = self.conn.conn.cursor()
        query = """DELETE FROM Chains WHERE chid = %s"""
        try:
            cursor.execute(query, (chid,))
            self.conn.conn.commit()
            return True
        except Exception:
            return False    
    
