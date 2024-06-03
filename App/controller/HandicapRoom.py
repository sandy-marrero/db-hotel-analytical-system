"""HandicapRoom Aggregate controller for project - hotel analytics system."""
from model.HandicapRoom import HandicapRoomDAO
from ETL.aggregate_representations import HandicapRoomModel
from flask import jsonify


class HandicapRoom:
    """Controller for HandicapRoom aggregate."""

    def getAggregate(hid: int, json) -> (str, int):
        """Get aggregate from HandicapRoomDAO by hotel primary key.

        :param hid: Primary for hotel table.
        :type hid: ``int``
        :param json: JSON from flask request
        :type json: ``json``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            dao: HandicapRoomDAO = HandicapRoomDAO()
        except Exception:
            return jsonify("Server is not available"), 503
        try:
            eid = int(json.get("eid"))
        except Exception:
            return jsonify("Invalid Request Body"), 400
        isAuthorized = dao.conn.isAuthorizedEmployee(hid, eid)
        if isAuthorized is False:
            return jsonify("Unauthorized User"), 403
        result = dao.getHandicapRoomReserveCountDAO(hid)
        if result is None:
            return jsonify(f"No hotel with ID {hid} was found"), 404
        else:
            result = list(
                map(
                    lambda x: HandicapRoomModel(rid=x[0],
                                                hid=x[1],
                                                rdid=x[2],
                                                rprice=x[3],
                                                reservation_count=x[4]).
                    __dict__, result))
            return jsonify(result)
