from model.PaymentMethod import PaymentMethodDAO
from ETL.aggregate_representations import PaymentMethodModel
from flask import jsonify

class PaymentMethod:

    def getPaymentMethod(self, json):
        try:
            dao: PaymentMethodDAO = PaymentMethodDAO()
        except Exception:
            return jsonify("Server is not available"), 503

        result = dao.getPaymentMethod()
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
            return jsonify("No valid results for Payment Methods"), 404
        else:
            result = list(
                map(
                    lambda x: PaymentMethodModel(payment_method=x[0],
                                                  count_payment=x[1],
                                                  payment_percentage=x[2]).
                    __dict__, result))
        return jsonify(result), 200
