from model.MostDiscount import MostDiscountDAO
from ETL.aggregate_representations import MostDiscountModel
from flask import jsonify

class MostDiscount:

    def getMostDiscount(hid: int, json) -> (str, int):
        try:
            dao: MostDiscountDAO = MostDiscountDAO()
        except Exception:
            return jsonify("Server is not available"), 503
        
        try:
            eid = int(json.get("eid"))
        except Exception:
            return jsonify("Invalid Request Body"), 400
        
        if dao.conn.isAuthorizedEmployee(hid, json.get("eid")) == False:
            return jsonify("Unauthorized user"), 403
        
        result = dao.getMostDiscountDAO(hid)
        if result is None:
            return jsonify(f"No hotel with ID {hid} was found"), 404
        else:
            result = list(
                map(
                    lambda x: MostDiscountModel(clid=x[0],
                                                  full_name=x[1],
                                                  discount=x[2]).
                    __dict__, result))
        return jsonify(result), 200