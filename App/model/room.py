"""Room table model for term project - hotel analytics system."""
from database.database import DatabaseConnection
from ETL.table_representations import RoomTableData, RoomTableDataNoPK
from typing import Optional, Iterable
from config.config import DatabaseConfiguration

config = DatabaseConfiguration()


class RoomDAO:
    """Data access object for room table."""

    def __init__(self):
        """Create RoomDAO Object and connect to database from config module.

        Will raise an exception if it cannot connect to the database.
        """
        try:
            self.conn = DatabaseConnection(config.DB_NAME, config.DB_USER,
                                           config.DB_PASS, config.DB_HOST,
                                           config.DB_PORT)
        except Exception as e:
            raise e

    def validateRoomNoPKEntry(self, room: RoomTableDataNoPK) -> bool:
        """Verify that the room data from a request is valid.

        Checks if Hotel and RoomDescription primary keys
        are inside the database.
        :param room: Pydantic Model for room table without primary key.
        :type room: ``RoomTableDataNoPK``
        :rtype: ``bool``
        """
        return self.conn.isHidInHotel(room.hid) and \
            self.conn.isRdidInRoomDescription(room.rdid) and \
            room.rprice >= 0

    def validateRoomEntry(self, room: RoomTableData) -> bool:
        """Verify that the room data from a request is valid.

        Checks if Hotel, RoomDescription and Room primary keys
        are inside the database.
        :param room: Pydantic Model for room table.
        :type room: ``RoomTableData``
        :rtype: ``bool``
        """
        return self.conn.isHidInHotel(room.hid) and \
            self.conn.isRdidInRoomDescription(room.rdid) and \
            room.rprice >= 0 and self.conn.isRidInRoom(room.rid)

    def getAllRooms(self) -> Optional[Iterable]:
        """Get all rooms from the rooms table.

        :rtype: ``Optional[Iterable]``
        """
        cursor = self.conn.conn.cursor()
        query = """SELECT rid, hid, rdid, rprice FROM room;"""
        cursor.execute(query)
        return cursor.fetchall()

    def getRoomById(self, rid: int) -> Optional[Iterable]:
        """Get a specific room using primary key.

        :param rid: Room table primary key.
        :type rid: ``int``
        :rtype: ``Optional[Iterable]``
        """
        cursor = self.conn.conn.cursor()
        query = """SELECT rid, hid, rdid, rprice FROM room
        WHERE rid = %s;"""
        cursor.execute(query, (rid, ))
        return cursor.fetchone()

    def createRoom(self, room: RoomTableDataNoPK) -> Optional[int]:
        """Create a room in the room table.

        Checks if Hotel and RoomDescription primary keys
        are inside the database.
        :param room: Pydantic Model for room table without primary key.
        :type room: ``RoomTableDataNoPK``
        :rtype: ``Optional[int]``
        """
        if self.validateRoomNoPKEntry(room) is False:
            return None
        cursor = self.conn.conn.cursor()
        query = """INSERT INTO room (hid, rdid, rprice)
                VALUES (%s,%s, %s) RETURNING rid;"""
        try:
            cursor.execute(query, (room.hid, room.rdid, room.rprice))
            self.conn.conn.commit()
            id = int(cursor.fetchone()[0])
            return id
        except Exception:
            return None

    def updateRoom(self, room: RoomTableData) -> Optional[int]:
        """Update existing room in room table.

        Checks if Hotel, RoomDescription and Room primary keys
        are inside the database.
        :param room: Pydantic Model for room table.
        :type room: ``RoomTableData``
        :rtype: ``Optional[int]``
        """
        if self.validateRoomEntry(room) is False:
            return None
        cursor = self.conn.conn.cursor()
        query = """UPDATE room SET hid = %s, rdid = %s, rprice = %s
        WHERE rid = %s RETURNING rid;"""
        try:
            cursor.execute(query, (room.hid, room.rdid, room.rprice, room.rid))
            self.conn.conn.commit()
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                return int(result[0])
        except Exception:
            return None

    def deleteRoom(self, rid: int) -> bool:
        """Delete room from room table.

        :param rid: Room table primary key.
        :type rid: ``int``
        :rtype: ``bool``
        """
        if self.conn.isRidInRoom(rid) is False:
            return False
        cursor = self.conn.conn.cursor()
        query = """DELETE from room WHERE rid = %s"""
        try:
            cursor.execute(query, (rid, ))
            self.conn.conn.commit()
            return True
        except Exception:
            return False
