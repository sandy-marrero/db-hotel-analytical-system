"""Database initialization and connection module.

This module was developed for the term project - hotel analytics systems for
CIIC4060/ICOM 5016.
"""
import psycopg2


class DatabaseConnection:
    """Connect to database."""

    def __init__(self, DB_NAME: str, DB_USER: str, DB_PASS: str, DB_HOST: str,
                 DB_PORT: str):
        """Create DatabaseConnection object.

        Will throw an exception if could not connect to database.
        """
        with psycopg2.connect(database=DB_NAME,
                              user=DB_USER,
                              password=DB_PASS,
                              host=DB_HOST,
                              port=DB_PORT) as conn:
            self.conn = conn

    def isRuidInRoomUnavailable(self, ruid: int) -> bool:
        """Check if primary key is in RoomUnavailable table."""
        cursor = self.conn.cursor()
        query = """SELECT * from roomunavailable where ruid = %s"""
        cursor.execute(query, (ruid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def isClidInClient(self, clid: int) -> bool:
        """Check if primary key is in client table."""
        cursor = self.conn.cursor()
        query = """SELECT * from client where clid = %s"""
        cursor.execute(query, (clid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def isReidInReserve(self, reid: int) -> bool:
        """Check if primary key is in reserve table."""
        cursor = self.conn.cursor()
        query = """SELECT * from reserve where reid = %s"""
        cursor.execute(query, (reid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def isRidInRoom(self, rid: int) -> bool:
        """Check if primary key is in room table."""
        cursor = self.conn.cursor()
        query = """SELECT * from room where rid = %s"""
        cursor.execute(query, (rid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def isHidInHotel(self, hid: int) -> bool:
        """Check if primary key is in hotel table."""
        cursor = self.conn.cursor()
        query = """SELECT * from hotel where hid = %s"""
        cursor.execute(query, (hid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def isRdidInRoomDescription(self, rdid: int) -> bool:
        """Check if primary key is in RoomDescription table."""
        cursor = self.conn.cursor()
        query = """SELECT * from roomdescription where rdid = %s"""
        cursor.execute(query, (rdid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True
        
    def isClidInClient(self, clid: int) -> bool:
        cursor = self.conn.cursor()
        query = """SELECT * from client where clid = %s"""
        cursor.execute(query, (clid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def isRuidInRoomUnavailable(self, ruid: int) -> bool:
        cursor = self.conn.cursor()
        query = """SELECT * from roomunavailable where ruid = %s"""
        cursor.execute(query, (ruid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def isAuthorizedEmployee(self, hid: int, eid: int) -> bool:
        """Check if an employee is from a hotel."""
        cursor = self.conn.cursor()
        if self.isHidInHotel(int(hid)) is False or \
        self.isEidInEmployee(eid) is False:
            return None
        query = "SELECT hid, position from employee where eid = %s"
        cursor.execute(query, (eid, ))
        employeeHid, employeePosition = cursor.fetchone()
        if employeePosition == 'Regular':
            return hid == employeeHid
        elif employeePosition == 'Supervisor':
            query = "SELECT chid from hotel where hid = %s;"
            cursor.execute(query, (hid, ))
            hotelChid = int(cursor.fetchone()[0])
            query = "SELECT chid from hotel where hid = %s;"
            cursor.execute(query, (employeeHid, ))
            employeeChid = int(cursor.fetchone()[0])
            return hotelChid == employeeChid
        elif employeePosition == 'Administrator':
            return True
        else:
            return False
    
    def isEidInEmployee(self, eid: int) -> bool:
        """Check if primary key is in employee table."""
        cursor = self.conn.cursor()
        query = """SELECT * from employee where eid = %s"""
        cursor.execute(query, (eid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True
        
    def isRidInRoomUnavailable(self, rid: int) -> bool:
        cursor = self.conn.cursor()
        query = """SELECT * from room where rid = %s"""
        cursor.execute(query, (rid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True
        
    def isChidInHotel(self, chid: int) -> bool:
        cursor = self.conn.cursor()
        query = """SELECT * from chains where chid = %s"""
        cursor.execute(query, (chid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def isEidInEmployee(self, eid: int) -> bool:
        """Check if primary key is in employee table."""
        cursor = self.conn.cursor()
        query = """SELECT * from employee where eid = %s"""
        cursor.execute(query, (eid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def isReservationConflict(self, rid: int, startdate: str, enddate: str) -> bool:
        if self.isRidInRoom(rid) == False:
            return False
        else:
            cursor = self.conn.cursor()
            query = """CREATE
            OR REPLACE FUNCTION CANRESERVE (
                RESERVATION_START_DATE DATE,
                RESERVATION_END_DATE DATE,
                RESERVATION_RID INTEGER
            ) RETURNS BOOLEAN AS $$
            DECLARE
                room_records integer;
            BEGIN
                select count(*) into room_records from roomunavailable where rid = reservation_rid and (startdate, enddate) overlaps (reservation_start_date, reservation_end_date);
                if (room_records >= 1) then
                return false;
                else
                return TRUE;
                end if;
            END;
            $$ LANGUAGE PLPGSQL; """
            cursor.execute(query)
            self.conn.commit()
            query = """select canreserve(date(%s), date(%s), %s)"""
            cursor.execute(query, (startdate, enddate, rid))
            result = cursor.fetchone()[0]
            return result
    
    def isLidInLogin(self, lid: int) -> bool:
        cursor = self.conn.cursor()
        query = """SELECT * from login where lid = %s"""
        cursor.execute(query, (lid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True
    def isChidInChains(self, chid:int) -> bool:
        cursor = self.conn.cursor()
        query = """SELECT * from chains where chid = %s"""
        cursor.execute(query, (chid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True
    def isEidInLogin(self, eid:int) -> bool:
        cursor = self.conn.cursor()
        query = """SELECT * from login where eid = %s"""
        cursor.execute(query, (eid, ))
        if cursor.fetchone() is None:
            return False
        else:
            return True