from typing import List, Tuple
import psycopg2
from database.database import DatabaseConnection
from config.config import DatabaseConfiguration

config = DatabaseConfiguration()


class EmployeeDAO:

    def __init__(self) -> None:
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e

    def getAll(self) -> List[Tuple[int, int, str, str, int, str, float]]:
        cursor = self.conn.conn.cursor()
        cursor.execute("SELECT * FROM Employee")
        employees = cursor.fetchall()
        return employees

    def getById(self, id) -> Tuple[int, int, str, str, int, str, float]:
        cursor = self.conn.conn.cursor()
        cursor.execute(f"SELECT * FROM Employee WHERE eid = {id}")
        employee = cursor.fetchone()
        return employee

    def update_Employee(self, id: int, hid: int, fname: str, lname: str, age: int, position: str, salary: float) -> None:
        if self.conn.isEidInEmployee(id) is False:
            return None
        cursor = self.conn.conn.cursor()
        cursor.execute(
            """UPDATE Employee SET hid = %s,
                                             fname = %s,
                                             lname = %s,
                                             age = %s,
                                             position = %s,
                                             salary = %s
                                             WHERE eid = %s
                                             returning eid""",
            (hid, fname, lname, age, position, salary, id))
        self.conn.conn.commit()
        return id

    def create_Employee(self, hid: int, fname: str, lname: str, age: str, position: str, salary: float) -> int:
        if self.conn.isHidInHotel(hid) == False:
            return None
        cursor = self.conn.conn.cursor()
        query = """INSERT INTO Employee (hid, fname, lname, age, position, salary) 
                   VALUES (%s, %s, %s, %s, %s, %s) returning eid"""
        try:
            cursor.execute(query, (hid, fname, lname, age, position, salary))
            self.conn.conn.commit()
            employee_id = cursor.fetchone()[0]
            return employee_id
        except Exception:
            return None

    def delete_Employee(self, eid: int) -> bool:
        if self.conn.isEidInEmployee(eid) is False:
            return False
        cursor = self.conn.conn.cursor()
        query = """DELETE from Employee where eid = %s"""
        try:
            cursor.execute(query, (eid, ))
            self.conn.conn.commit()
            return True
        except Exception:
            return False
