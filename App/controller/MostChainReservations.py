from model.MostChainReservations import MostChainReservationsDAO
from ETL.aggregate_representations import MostChainReservationsModel
from flask import jsonify

class MostChainReservations:

    def getMostChainReservations(self, json):
        try:
            dao: MostChainReservationsDAO = MostChainReservationsDAO()
        except Exception:
            return jsonify("Server is not available"), 503

        result = dao.getMostChainReservations()
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
                    lambda x: MostChainReservationsModel(chain_name=x[0],
                                                  reservation_month=x[1],
                                                  reservation_count=x[2]).
                    __dict__, result))
        return jsonify(result), 200