from model.MostClientCapacity import MostClientCapacityDAO
from ETL.aggregate_representations import MostClientCapacityModel
from flask import jsonify

class MostClientCapacity:

    def getMostClientCapacity(self, json):
        try:
            dao: MostClientCapacityDAO = MostClientCapacityDAO()
        except Exception:
            return jsonify("Server is not available"), 503

        result = dao.getMostClientCapacity()
        try:
            eid = json.get("eid")
            if eid is None:
                return jsonify("No eid in request"), 400
            if not isinstance(eid, int):
                return jsonify("Invalid type for eid"), 400
        except Exception:
            return jsonify("No eid in request"), 400

        if int(eid) != -1:
            return jsonify("Unauthorized User"), 403

        if result is None:
            return jsonify("No valid results for Client Capacity"), 404
        else:
            result = list(
                map(
                    lambda x: MostClientCapacityModel(hotel_name=x[0],
                                                  total_capacity=x[1]).
                    __dict__, result))
        return jsonify(result), 200