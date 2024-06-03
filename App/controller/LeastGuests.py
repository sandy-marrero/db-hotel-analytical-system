from model.LeastGuests import LeastGuestsDAO
from ETL.aggregate_representations import LeastGuestsModel
from flask import jsonify

class LeastGuests:

    def getLeastGuests(hid: int, json) -> (str, int):
        try:
            dao: LeastGuestsDAO = LeastGuestsDAO()
        except Exception:
            return jsonify("Server is not available"), 503
        
        try:
            eid = int(json.get("eid"))
        except Exception:
            return jsonify("Invalid Request Body"), 400
        
        if dao.conn.isAuthorizedEmployee(hid, json.get("eid")) == False:
            return jsonify("Unauthorized user"), 403
        
        result = dao.getLeastGuestsDAO(hid)
        
        if result is None:
            return jsonify(f"No hotel with ID {hid} was found"), 404
        else:
            result = list(
                map(
                    lambda x: LeastGuestsModel(rid=x[0],
                                                  capacity=x[1]).
                    __dict__, result))
        return jsonify(result), 200
