"""MostCreditCard Aggregate controller for project - hotel analytics system."""
from model.MostCreditCard import MostCreditCardDAO
from ETL.aggregate_representations import MostCreditCardModel
from flask import jsonify


class MostCreditCard:
    """Controller for MostCreditCard aggregate."""

    def getAggregate(hid: int, json) -> (str, int):
        """Get aggregate from MostCreditCardDAO by hotel primary key.

        :param hid: Primary for hotel table.
        :type hid: ``int``
        :param json: JSON from flask request
        :type json: ``json``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            dao: MostCreditCardDAO = MostCreditCardDAO()
        except Exception:
            return jsonify("Server is not available"), 503
        try:
            eid = int(json.get("eid"))
        except Exception:
            return jsonify("Invalid Request Body"), 400
        isAuthorized = dao.conn.isAuthorizedEmployee(hid, eid)
        if isAuthorized is False:
            return jsonify("Unauthorized User"), 403
        result = dao.getMostCreditCards(hid)
        if result is None:
            return jsonify(f"No hotel with ID {hid} was found"), 404
        else:
            result = list(
                map(
                    lambda x: MostCreditCardModel(clid=x[0],
                                                  fname=x[1],
                                                  lname=x[2],
                                                  age=x[3],
                                                  memberyear=x[4],
                                                  reservation_count=x[5]).
                    __dict__, result))
            return jsonify(result)
