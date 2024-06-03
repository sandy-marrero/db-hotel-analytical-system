"""HighestPaid Aggregate controller for project - hotel analytics system."""
from model.HighestPaid import HighestPaidDAO
from ETL.aggregate_representations import HighestPaidModel
from flask import jsonify


class HighestPaid:
    """Controller for HighestPaid aggregate."""

    def getAggregate(hid: int, json) -> (str, int):
        """Get aggregate from HighestPaidDAO by hotel primary key.

        :param hid: Primary for hotel table.
        :type hid: ``int``
        :param json: JSON from flask request
        :type json: ``json``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            dao: HighestPaidDAO = HighestPaidDAO()
        except Exception:
            return jsonify("Server is not available"), 503
        try:
            eid = int(json.get("eid"))
        except Exception:
            return jsonify("Invalid Request Body"), 400
        isAuthorized = dao.conn.isAuthorizedEmployee(hid, eid)
        if isAuthorized is False:
            return jsonify("Unauthorized User"), 403
        result = dao.getHighestPaid(hid)
        if result is None:
            return jsonify(f"No hotel with ID {hid} was found"), 404
        else:
            result = list(
                map(
                    lambda x: HighestPaidModel(eid=x[0],
                                               hid=x[1],
                                               fname=x[2],
                                               lname=x[3],
                                               age=x[4],
                                               salary=x[5]).__dict__, result))
            return jsonify(result)
