"""Room table controller for term project - hotel analytics system."""
from model.room import RoomDAO
from ETL.table_representations import RoomTableData, RoomTableDataNoPK
from flask import jsonify


class Room:
    """Controller from room table."""

    def getAllRooms() -> (str, int):
        """Get all rooms from RoomDAO.

        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            dao = RoomDAO()
        except Exception:
            return jsonify("Server is not available"), 503
        result = dao.getAllRooms()
        if result is None:
            return jsonify("No Room found"), 404
        else:
            result = list(
                map(
                    lambda x: RoomTableData(
                        rid=x[0], hid=x[1], rdid=x[2], rprice=x[3]).__dict__,
                    result))
            return jsonify(result)

    def getRoomById(rid: int) -> (str, int):
        """Get rooms from RoomDAO by primary key.

        :param rid: Primary for room table.
        :type rid: ``int``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            dao = RoomDAO()
        except Exception:
            return jsonify("Server is not available"), 503
        result = dao.getRoomById(rid)
        if result is None:
            return jsonify(f"No room with ID {rid} was found."), 404
        else:
            result = RoomTableData(rid=result[0],
                                   hid=result[1],
                                   rdid=result[2],
                                   rprice=result[3]).__dict__
            return jsonify(result)

    def createRoom(json) -> (str, int):
        """Create room into RoomDAO.

        :param json: JSON from flask request
        :type json: ``json``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            room: RoomTableDataNoPK = RoomTableDataNoPK(
                hid=json.get('hid'),
                rdid=json.get('rdid'),
                rprice=json.get('rprice'))
            try:
                dao: RoomDAO = RoomDAO()
            except Exception:
                return jsonify("Server is not available"), 503
            result = dao.createRoom(room)
            if result is None:
                return jsonify("Room could not be created"), 500
            else:
                return jsonify({"rid": int(result)})
        except Exception:
            return jsonify("Invalid request body"), 400

    def updateRoom(rid: int, json: str) -> (str, int):
        """Create room into RoomDAO.

        :param rid: Primary key from room table
        :type rid: ``int``
        :param json: JSON from flask request
        :type json: ``json``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            room: RoomTableData = RoomTableData(rid=rid,
                                                hid=json.get('hid'),
                                                rdid=json.get('rdid'),
                                                rprice=json.get('rprice'))
            try:
                dao: RoomDAO = RoomDAO()
            except Exception:
                return jsonify("Server is not available"), 503
            result = dao.updateRoom(room)
            if result is None:
                return jsonify("Room could not be updated"), 500
            else:
                return jsonify({"rid": int(result)})
        except Exception:
            return jsonify("Invalid request body"), 400

    def deleteRoom(rid: int):
        """Delete room into RoomDAO.

        :param rid: Primary key from room table
        :type rid: ``int``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            rid = int(rid)
            try:
                dao: RoomDAO = RoomDAO()
            except Exception:
                return jsonify("Server is not available"), 503
            if dao.deleteRoom(rid) is False:
                return jsonify(
                    f"Room with ID {rid} could not be deleted."), 404
            else:
                return jsonify(rid)
        except Exception:
            return jsonify(f"Room with ID {rid} could not be deleted."), 404
