"""Reserve table model for term project - hotel analytics system."""
from database.database import DatabaseConnection
from ETL.table_representations import ReserveTableDataNoPK, ReserveTableData
from typing import Optional, Iterable
from config.config import DatabaseConfiguration
from datetime import datetime

config = DatabaseConfiguration()


class ReserveDAO:
    """Data access object for reserve table."""

    def __init__(self):
        """Create ReserveDAO Object and connect to database from config module.

        Will raise an exception if it cannot connect to the database.
        """
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e

    def isValidPayment(self, payment: str) -> bool:
        """Validate payment method string to match enum.

        :param payment: Payment string from Reserve entry.
        :type payment: ``str``
        :rtype: ``bool``
        """
        match payment:
            case 'cash':
                return True
            case 'credit card':
                return True
            case 'check':
                return True
            case 'debit card':
                return True
            case 'pear pay':
                return True
            case _:
                return False

    def validateReserveNoPKEntry(self, request: ReserveTableDataNoPK) -> bool:
        """Validate if request is valid.

        Check if RoomUnavailable and Reserve primary keys are in
        database and if total_cost, guests and payment are valid.
        :rtype: ``bool``
        """
        return self.conn.isRuidInRoomUnavailable(
            request.ruid
        ) and self.conn.isClidInClient(
            request.clid
        ) and request.guests >= 1 \
            and self.isValidPayment(request.payment)

    def validateReserveEntry(self, request: ReserveTableData) -> bool:
        """Validate if request is valid.

        Check if RoomUnavailable, Reserve primary keys are in
        database and if total_cost, guests and payment are valid.
        :rtype: ``bool``
        """
        return self.conn.isClidInClient(request.clid) and \
            self.conn.isRuidInRoomUnavailable(request.ruid) and \
            self.conn.isReidInReserve(request.reid) and \
            request.total_cost >= 0 and request.guests >= 1 and \
            self.isValidPayment(request.payment)

    def getAllReservations(self) -> Optional[Iterable]:
        """Get all reservations from reserve table.

        :rtype: ``Optional[Iterable]``
        """
        cursor = self.conn.conn.cursor()
        query = """SELECT reid, ruid, clid,
        total_cost, payment, guests FROM reserve;"""
        cursor.execute(query)
        return cursor.fetchall()

    def getReservationById(self, reid: int) -> Optional[Iterable]:
        """Get a reservation by primary key.

        :param reid: Reserve table primary key
        :type reid: ``int``
        :rtype: ``Optional[Iterable]``
        """
        cursor = self.conn.conn.cursor()
        query = """SELECT reid, ruid, clid,
        total_cost, payment, guests FROM reserve
        where reid = %s;"""
        cursor.execute(query, (reid, ))
        return cursor.fetchone()

    def createReservation(self,
                          reservation: ReserveTableDataNoPK) -> Optional[int]:
        """Create a reservation reserve table.

        :param reservation: Reserve table model without primary key
        :type reservation: ``ReserveTableDataNoPK``
        :rtype: ``Optional[int]``
        """
        if self.validateReserveNoPKEntry(reservation) is False:
            return None
        cursor = self.conn.conn.cursor()
        query = """
                SELECT
        rprice,
	memberyear,
        startdate,
        enddate,
	springmkup,
	summermkup,
	fallmkup,
	wintermkup
        FROM
	roomunavailable
        NATURAL INNER JOIN room
        NATURAL INNER JOIN hotel
        NATURAL INNER JOIN chains
	NATURAL INNER JOIN client
        WHERE
        ruid = %s and clid = %s;

        """
        try:
            cursor.execute(query, (reservation.ruid, reservation.clid))
            self.conn.conn.commit()
            rprice, memberyear , reservationstartdate, reservationenddate, springmkup, summermkup, fallmkup, wintermkup = cursor.fetchone()
        except Exception:
            return None
        markup: float = float()
        if reservationstartdate.month >= 3 and reservationstartdate.month <= 5:
            markup = springmkup
        elif reservationstartdate.month >=6 and reservationstartdate.month <=8:
            markup = summermkup
        elif reservationstartdate.month >= 9 and reservationstartdate <= 11:
            markup = fallmkup
        else:
            markup = wintermkup
        discount: float = float()
        if memberyear <= 4:
            discount = 0.98
        elif memberyear >= 5 and memberyear <= 9:
            discount = 0.95
        elif memberyear >= 10 and memberyear <= 14:
            discount = 0.92
        else:
            discount = 0.88


        reservationdaydelta = (reservationenddate - reservationstartdate).days

        total_cost = rprice*reservationdaydelta*markup*discount
        
        query = """INSERT INTO RESERVE (ruid, clid,
                total_cost, payment, guests)
                VALUES (%s,%s,%s,%s,%s) RETURNING reid;"""
        try:
            cursor.execute(
                query,
                (reservation.ruid, reservation.clid, total_cost,
                 reservation.payment, reservation.guests))
            self.conn.conn.commit()
            id = int(cursor.fetchone()[0])
            return id
        except Exception:
            return None

    def updateReservation(self,
                          reservation: ReserveTableData) -> Optional[int]:
        """Update a reservation reserve table.

        :param reservation: Reserve table model with primary key
        :type reservation: ``ReserveTableData``
        :rtype: ``Optional[int]``
        """
        if self.validateReserveEntry(reservation) is False:
            return None
        cursor = self.conn.conn.cursor()
        query = """UPDATE reserve SET ruid = %s, clid = %s, total_cost = %s,
        payment = %s, guests = %s where reid = %s returning reid;"""
        try:
            cursor.execute(query, (
                reservation.ruid,
                reservation.clid,
                reservation.total_cost,
                reservation.payment,
                reservation.guests,
                reservation.reid,
            ))
            self.conn.conn.commit()
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                return int(result[0])
        except Exception:
            return None

    def deleteReservation(self, reid: int) -> bool:
        """Delete a reservation by primary key.

        :param reid: Reserve table primary key
        :type reid: ``int``
        :rtype: ``bool``
        """
        if self.conn.isReidInReserve(reid) is False:
            return False
        cursor = self.conn.conn.cursor()
        query = """DELETE from reserve where reid = %s"""
        try:
            cursor.execute(query, (reid, ))
            self.conn.conn.commit()
            return True
        except Exception:
            return False
