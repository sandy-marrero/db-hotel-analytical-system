"""LeastReserve Aggregate controller for project - hotel analytics system."""
from model.LeastReserve import LeastReserveDAO
from ETL.aggregate_representations import LeastReserveModel
from flask import jsonify


class LeastReserve:
    """Controller for LeastReserve aggregate."""

    def getAggregate(hid: int, json) -> (str, int):
        """Get aggregate from LeastReserveDAO by hotel primary key.

        :param hid: Primary for hotel table.
        :type hid: ``int``
        :param json: JSON from flask request
        :type json: ``json``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            dao: LeastReserveDAO = LeastReserveDAO()
        except Exception:
            return jsonify("Server is not available"), 503
        try:
            eid = int(json.get("eid"))
        except Exception:
            return jsonify("Invalid Request Body"), 400
        isAuthorized = dao.conn.isAuthorizedEmployee(hid, eid)
        if isAuthorized is False:
            return jsonify("Unauthorized User"), 403
        result = dao.getLeastRooms(hid)
        if result is None:
            return jsonify(f"No hotel with ID {hid} was found"), 404
        else:
            result = list(
                map(
                    lambda x: LeastReserveModel(rid=x[0],
                                                hid=x[1],
                                                rdid=x[2],
                                                rprice=x[3],
                                                days_reserved=x[4]).__dict__,
                    result))
            return jsonify(result)
