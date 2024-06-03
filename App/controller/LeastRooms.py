from model.LeastRooms import LeastRoomsDAO
from ETL.aggregate_representations import LeastRoomsModel
from flask import jsonify


class LeastRooms:

    def getLeastRooms(self, json):
        try:
            dao: LeastRoomsDAO = LeastRoomsDAO()
        except Exception:
            return jsonify("Server is not available"), 503

        result = dao.getLeastRooms()

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
            return jsonify("No valid results for Least Rooms"), 404
        else:
            result = list(
                map(
                    lambda x: LeastRoomsModel(chain_name=x[0],num_rooms=x[1]).
                    __dict__, result))
        return jsonify(result), 200
