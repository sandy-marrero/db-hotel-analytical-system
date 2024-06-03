"""Data extraction module for csv, xlsx, sqlite and json files for Phase 1.

This module was developed for the term project - Hotel Analytics Systems for
CIIC4060/ICOM 5016. This module is exclusively for implementing the objectives
in phase 1 of the project.
"""
import sqlite3
from typing import List
from db import DatabaseConnection
import pandas as pd
from pydantic import BaseModel, field_validator
from table_representations import ReserveTableData, RoomTableData, \
    RoomDescriptionTableData, LoginTableData, ChainsTableData, \
    EmployeeTableData, ClientTableData, HotelTableData, \
    RoomUnavailableTableData
import re


class ReserveTableRawData:
    """Class to connect to reserve.db sqlite database and sanitize entries."""

    def __init__(self):
        """Connect to reserve.db database and sanitize input."""
        self.conn = sqlite3.connect("./Raw_Data/reservations.db")
        self.cursor = self.conn.cursor()
        raw_data = self.cursor.execute("""select reid,
        ruid, clid, total_cost, payment, guests from reserve;""").fetchall()
        raw_data: List[ReserveTableData] = list(
            map(
                lambda x: ReserveTableData(reid=x[0],
                                           ruid=x[1],
                                           clid=x[2],
                                           total_cost=x[3],
                                           payment=x[4],
                                           guests=x[5]), raw_data))
        self.cleanData = self.sanitizeData(raw_data)

    def __del__(self):
        """Disconnect from reserve.db sqlite database."""
        self.conn.close()

    def sanitizeData(
            self, raw_data: List[ReserveTableData]) -> List[ReserveTableData]:
        """Remove invalid (dirty) data for insertion into the database."""
        return list(
            filter(
                lambda x: x.reid is not None and x.ruid is not None and x.clid
                is not None and x.total_cost is not None and x.payment is
                not None and x.payment != "" and x.guests is not None and x.
                guests >= 1, raw_data))

    def getCleanData(self) -> List[ReserveTableData]:
        """Get sanitized records from records.db sqlite database."""
        return self.cleanData

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Reserve table.

        Alters Reserve table by adding primary key constraint to reid.
        Reset sequence to max after all data has been inserted.
        """
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO RESERVE (reid, ruid, clid,
                total_cost, payment, guests)
                VALUES (%s,%s,%s,%s,%s,%s)""",
                (record.reid, record.ruid, record.clid, record.total_cost,
                 record.payment, record.guests))
        conn.cursor.execute("""ALTER TABLE reserve ADD PRIMARY KEY (reid);""")
        conn.conn.commit()
        conn.cursor.execute("select max(reid) from reserve;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE reserve_reid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()


class RoomTableRawData:
    """Class to connect to rooms.db sqlite database and sanitize records."""

    def __init__(self):
        """Connect to rooms.db database and sanitize input."""
        self.conn = sqlite3.connect("./Raw_Data/rooms.db")
        self.cursor = self.conn.cursor()
        raw_data = self.cursor.execute("""
        select rid, hid, rdid, rprice from Room;""").fetchall()
        raw_data = list(
            map(
                lambda x: RoomTableData(
                    rid=x[0], hid=x[1], rdid=x[2], rprice=x[3]), raw_data))
        self.cleanData = self.sanitizeData(raw_data)

    def __del__(self):
        """Disconnect from rooms.db sqlite database."""
        self.conn.close()

    def sanitizeData(self, raw_data: List[RoomTableData]):
        """Remove invalid (dirty) data for insertion into the database."""
        return list(
            filter(
                lambda x: x.rid is not None and x.hid is not None and x.rdid is
                not None and x.rprice is not None and x.rprice > 0, raw_data))

    def insertSanitizedRecords(self, conn: DatabaseConnection):
        """Insert clean data into the Room table.

        Alters Reserve table by adding primary key constraint to rid.
        Reset sequence to max after all data has been inserted.
        """
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO Room
                (rid, hid, rdid, rprice)
                VALUES (%s,%s,%s,%s)""",
                (record.rid, record.hid, record.rdid, record.rprice))
        conn.cursor.execute("""ALTER TABLE Room ADD PRIMARY KEY (rid);""")
        conn.conn.commit()
        conn.cursor.execute("select max(rid) from room;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE room_rid_seq
        restart with %s;""", (max, ))

    def getCleanData(self) -> List[ReserveTableData]:
        """Get sanitized records from rooms.db sqlite database."""
        return self.cleanData


class RoomDescriptionTableRawData:
    """Class to open dataframe for Room Details JSON and sanitize records."""

    def __init__(self):
        """Read JSON File and sanitize input."""
        self.roomDescription_data = list()
        try:
            df = pd.read_json("Raw_Data/roomdetails.json")
            df = df.dropna()
            df['detailid'] = df['detailid'].astype(int)
            for index, row in df.iterrows():
                self.roomDescription_data.append(
                    RoomDescriptionTableData(rdid=row['detailid'],
                                             rname=row['name'],
                                             rtype=row['type'],
                                             capacity=row['capacity'],
                                             ishandicap=bool(row['handicap'])))
        except Exception as e:
            print("Unable to read JSON", e)
            return None

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the RoomDescription table.

        Reset sequence to max after all data has been inserted.
        """
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO RoomDescription
                (rdid, rname, rtype, capacity, ishandicap)
                VALUES (%s,%s,%s,%s,%s)""",
                (record.rdid, record.rname, record.rtype, record.capacity,
                 record.ishandicap))
        conn.conn.commit()

        conn.cursor.execute("select max(rdid) from roomdescription;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE roomdescription_rdid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()

    def getCleanData(self) -> List[RoomDescriptionTableData]:
        """Return sanitized roomDescriptionData."""
        return self.roomDescription_data


class LoginTableRawData:
    """Class to open dataframe for Login XLSX and sanitize records."""

    def __init__(self):
        """Read Excel File and sanitize input."""
        self.login_data = list()
        try:
            df = pd.read_excel("Raw_Data/login.xlsx")
            df = df.dropna()
            df['lid'] = df['lid'].astype(int)
            for index, row in df.iterrows():
                self.login_data.append(
                    LoginTableData(lid=row['lid'],
                                   eid=row['employeeid'],
                                   username=row['user'],
                                   password=row['pass']))
        except Exception as e:
            print("Unable to read XLSX", e)
            return None

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Login table.

        Reset sequence to max after all data has been inserted.
        """
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO Login
                (lid, eid, username, password)
                VALUES (%s,%s,%s,%s)""",
                (record.lid, record.eid, record.username, record.password))
        conn.conn.commit()

        conn.cursor.execute("select max(lid) from login;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE login_lid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()

    def getCleanData(self) -> List[LoginTableData]:
        """Return sanitized LoginTableData."""
        return self.login_data


class EmployeeTableRawData:
    """Class to open dataframe for Employee JSON and sanitize records."""

    def __init__(self):
        """Read JSON File and sanitize input."""
        self.employee_data = list()
        try:
            df = pd.read_json("Raw_Data/employee.json")
            df = df.dropna()
            df['employeeid'] = df['employeeid'].astype(int)
            for index, row in df.iterrows():
                self.employee_data.append(
                    EmployeeTableData(eid=row['employeeid'],
                                      hid=row['hotelid'],
                                      fname=row['firstname'],
                                      lname=row['lastname'],
                                      age=row['age'],
                                      position=row['position'],
                                      salary=row['salary']))
        except Exception as e:
            print("Unable to read JSON", e)
            return None

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Employee table.

        Reset sequence to max after all data has been inserted.
        """
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO Employee
                (eid, hid, fname, lname, age, position, salary)
                VALUES (%s,%s,%s, %s,%s,%s,%s)""",
                (record.eid, record.hid, record.fname, record.lname,
                 record.age, record.position, record.salary))
        conn.conn.commit()

        conn.cursor.execute("select max(eid) from employee;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE employee_eid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()

    def getCleanData(self) -> List[EmployeeTableData]:
        """Return Sanitize EmployeeTableData."""
        return self.employee_data


class ChainsTableRawData:
    """Class to open dataframe for Chains XLSX file and sanitize records."""

    def __init__(self):
        """Read Excel File and sanitize input."""
        self.chains_data = list()
        try:
            df = pd.read_excel("Raw_Data/chain.xlsx")
            df = df.dropna()
            df['id'] = df['id'].astype(int)
            for index, row in df.iterrows():
                self.chains_data.append(
                    ChainsTableData(chid=row['id'],
                                    cname=row['name'],
                                    springmkup=row['spring'],
                                    summermkup=row['summer'],
                                    fallmkup=row['fall'],
                                    wintermkup=row['winter']))
        except Exception as e:
            print("An error occurred:", e)
            return None

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Chains table.

        Reset sequence to max after all data has been inserted.
        """
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO Chains
                (chid, cname, springmkup, summermkup, fallmkup, wintermkup)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (record.chid, record.cname, record.springmkup,
                 record.summermkup, record.fallmkup, record.wintermkup))
        conn.conn.commit()

        conn.cursor.execute("select max(chid) from chains;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE chains_chid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()

    def getCleanData(self) -> List[ChainsTableData]:
        """Return sanitized ChainsTableData."""
        return self.chains_data


class ClientTableRawData:
    """Accesses the clients.csv file, sanitizes and inserts the entries."""

    def __init__(self):
        """Access the clients.csv file and sanitizes the input."""
        df = pd.read_csv('./Raw_Data/client.csv')
        df = df.dropna()
        raw_data = list()
        for index, row in df.iterrows():
            raw_data.append(
                ClientTableData(clid=row['clid'],
                                fname=row[' fname'],
                                lname=row[' lastname'],
                                age=row[' age'],
                                memberyear=row[' memberyear']))
        self.cleanData = self.sanitizeData(raw_data)

    def sanitizeData(self,
                     raw_data: List[ClientTableData]) -> List[ClientTableData]:
        """Remove invalid (dirty) data for insertion into the database."""
        return list(
            # Filters out null values
            filter(
                lambda x: x.clid is not None and x.fname is not None and x.
                lname is not None and x.age is not None and x.memberyear is
                not None, raw_data))

    def getCleanData(self) -> List[ClientTableData]:
        """Get sanitized records from clients.csv file."""
        return self.cleanData

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Client table.

        Reset sequence to max after all data has been inserted.
        """
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO CLIENT (clid, fname, lname, age, memberyear)
                VALUES(%s, %s, %s, %s, %s)""",
                (record.clid, record.fname, record.lname, record.age,
                 record.memberyear))
            conn.conn.commit()
        conn.cursor.execute("select max(clid) from client;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE client_clid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()


class HotelTableRawData:
    """Class accesses the hotel.csv file, sanitizes and inserts the entries."""

    def __init__(self):
        """Access the clients.csv file and sanitizes the input."""
        df = pd.read_csv('./Raw_Data/hotel.csv')
        df = df.dropna()
        raw_data = list()
        for index, row in df.iterrows():
            raw_data.append(
                HotelTableData(hid=row['hid'],
                               chid=row['chain'],
                               hname=row['name'],
                               hcity=row['city']))
        self.cleanData = self.sanitizeData(raw_data)

    def sanitizeData(self,
                     raw_data: List[HotelTableData]) -> List[HotelTableData]:
        """Remove invalid (dirty) data for insertion into the database."""
        return list(
            # Filters out null values
            filter(
                lambda x: x.hid is not None and x.chid is not None and x.hname
                is not None and x.hcity is not None, raw_data))

    def getCleanData(self) -> List[HotelTableData]:
        """Get sanitized records from hotel.csv file."""
        return self.cleanData

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Hotel table.

        Reset sequence to max after all data has been inserted.
        """
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO HOTEL (hid, chid, hname, hcity)
                VALUES(%s, %s, %s, %s)""",
                (record.hid, record.chid, record.hname, record.hcity))
            conn.conn.commit()
        conn.cursor.execute("select max(hid) from hotel;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE hotel_hid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()


class RoomUnavailableTableData(BaseModel):
    """Class to represent the records inside the RoomUnavailable table.

    Create for the RoomUnavailable class.

    :param ruid: (int): Serial Primary key for RoomUnavailable table
    :param rid: (int): INteger Foreign key from Room table
    :param startdate: (date): DATE, represents start date of room reservation
    :param enddate: (date): DATE, represents end date of room reservation
    """

    ruid: int
    rid: int
    startdate: str
    enddate: str

    @field_validator("startdate", "enddate")
    @classmethod
    def validate_date(cls, value):
        """Validate that start and end date are valid."""
        if not re.match(r"\d+-\d+-\d+", value):
            raise ValueError(f"Invalid date string: {value}")
        year = int(value.split("-")[0])
        month = int(value.split("-")[1])
        day = int(value.split("-")[2])
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month: {month}")
        elif day < 1 or day > 31:
            raise ValueError(f"Invalid day: {day}")
        elif year < 1:
            raise ValueError(f"Invalid year {year}")
        return value

    def __str__(self) -> str:
        """Return string representation of RoomUnavailableTableData Class."""
        s = (f"{self.ruid}-{self.rid}-{self.startdate}-{self.enddate}")
        return s


class RoomUnavailableTableRawData:
    """Accesses room_unavailable.csv file, sanitize and inserts the entries."""

    def __init__(self):
        """Access the room_unavaible.csv file and sanitizes the input."""
        df = pd.read_csv('./Raw_Data/room_unavailable.csv')
        df = df.dropna()
        raw_data = list()
        for index, row in df.iterrows():
            raw_data.append(
                RoomUnavailableTableData(ruid=row['ruid'],
                                         rid=row['rid'],
                                         startdate=row['startdate'],
                                         enddate=row['enddate']))
        self.cleanData = self.sanitizeData(raw_data)

    def sanitizeData(
        self, raw_data: List[RoomUnavailableTableData]
    ) -> List[RoomUnavailableTableData]:
        """Remove invalid (dirty) data for insertion into the database."""
        return list(
            # Filters out null values
            filter(
                lambda x: x.ruid is not None and x.rid is not None and x.
                startdate is not None and x.enddate is not None, raw_data))

    def getCleanData(self) -> List[RoomUnavailableTableData]:
        """Get sanitized records from room_unavailable.csv file."""
        return self.cleanData

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Get sanitized records from room_unavailable.csv file.

        Reset sequence to max after all data has been inserted.
        """
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO ROOMUNAVAILABLE (ruid, rid, startdate, enddate)
                VALUES(%s, %s, %s, %s)""",
                (record.ruid, record.rid, record.startdate, record.enddate))
            conn.conn.commit()
        conn.cursor.execute("select max(ruid) from roomunavailable;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE roomunavailable_ruid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()


if __name__ == "__main__":
    conn = DatabaseConnection(
        "d14415u410n5rb", "xnfsmenglhinzl",
        "d3d73ac8955dedf8ca211716cdaf50136e69d4f14e6b0dd1782ed6a119d16d7a",
        "ec2-23-22-188-47.compute-1.amazonaws.com", "5432")
    loginData = LoginTableRawData()
    loginData.insertSanitizedData(conn)
    employeeData = EmployeeTableRawData()
    employeeData.insertSanitizedData(conn)
    hotelData = HotelTableRawData()
    hotelData.insertSanitizedData(conn)
    chainsData = ChainsTableRawData()
    chainsData.insertSanitizedData(conn)
    roomDescriptionData = RoomDescriptionTableRawData()
    roomDescriptionData.insertSanitizedData(conn)
    clientData = ClientTableRawData()
    clientData.insertSanitizedData(conn)
    roomData = RoomTableRawData()
    roomData.insertSanitizedRecords(conn)
    reserveData = ReserveTableRawData()
    reserveData.insertSanitizedData(conn)
    roomUnavailableData = RoomUnavailableTableRawData()
    roomUnavailableData.insertSanitizedData(conn)
    conn.addForeignKeyConstraints()
