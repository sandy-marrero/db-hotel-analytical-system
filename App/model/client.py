from typing import List, Tuple
from config.config import DatabaseConfiguration
from database.database import DatabaseConnection

import psycopg2


class ClientDAO:

    def __init__(self):
        self.conn = DatabaseConnection(DB_HOST=DatabaseConfiguration.DB_HOST,
                                       DB_NAME=DatabaseConfiguration.DB_NAME,
                                       DB_USER=DatabaseConfiguration.DB_USER,
                                       DB_PASS=DatabaseConfiguration.DB_PASS,
                                       DB_PORT=DatabaseConfiguration.DB_PORT)

    def validateClientEntry(self, clid) -> bool:
        return self.conn.isClidInClient(clid)

    def getAll(self) -> List[Tuple[int, str, str, int, int]]:
        cursor = self.conn.conn.cursor()
        cursor.execute("SELECT * FROM Client")
        client = cursor.fetchall()
        return client

    def getById(self, id) -> Tuple[int, str, str, int, int]:
        cursor = self.conn.conn.cursor()
        cursor.execute(f"SELECT * FROM Client WHERE clid = {id}")
        client = cursor.fetchone()
        return client

    def addClient(self, fname: str, lname: str, age: int,
                  memberyear: int) -> int:
        cursor = self.conn.conn.cursor()
        cursor.execute(
            "INSERT INTO Client (fname, lname, age, memberyear) VALUES (%s, %s, %s, %s) RETURNING clid",
            (fname, lname, age, memberyear))
        client_id = cursor.fetchone()[0]
        self.conn.conn.commit()
        return client_id

    def updateClient(self, id: int, fname: str, lname: str, age: int,
                     memberyear: int) -> None:
        if self.validateClientEntry(id) is False:
            return False
        cursor = self.conn.conn.cursor()
        cursor.execute(
            "UPDATE Client SET fname = %s, lname = %s, age = %s, memberyear = %s WHERE clid = %s",
            (fname, lname, age, memberyear, id))
        self.conn.conn.commit()
        return id

    def deleteClient(self, clid: int) -> bool:
        if self.conn.isClidInClient(clid) == False:
            return False
        cursor = self.conn.conn.cursor()
        query = """DELETE from client where clid = %s"""
        try:
            cursor.execute(query, (clid, ))
            self.conn.conn.commit()
            return True
        except Exception:
            return False
