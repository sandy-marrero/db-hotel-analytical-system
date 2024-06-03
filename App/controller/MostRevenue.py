#SELECT c.chain_name, SUM(r.total_cost) AS total_revenue
# FROM chains c
# JOIN hotel h ON c.chain_id = h.chain_id
# JOIN reserve r ON h.hotel_id = r.hotel_id
# GROUP BY c.chain_name
# ORDER BY total_revenue DESC
# LIMIT 3;
from model.MostRevenue import MostRevenueDAO
from ETL.aggregate_representations import MostRevenueModel
from flask import jsonify


class MostRevenue:

    def getAggregate(self,json) -> (str, int):
        try:
            dao: MostRevenueDAO = MostRevenueDAO()
        except Exception:
            return jsonify("Server is not available"), 503

        result = dao.getMostRevenue()

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
            return jsonify("No valid results for Most Revenue"), 404
        else:
            result = list(
                map(
                    lambda x: MostRevenueModel(chain_name=x[0],
                                                  total_revenue=x[1]).
                    __dict__, result))
        return jsonify(result), 200
