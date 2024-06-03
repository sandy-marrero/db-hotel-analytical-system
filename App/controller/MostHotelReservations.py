from model.MostHotelReservations import MostHotelReservationsDAO
from ETL.aggregate_representations import MostHotelReservationsModel
from flask import jsonify

class MostHotelReservations:

    def getMostHotelReservations(self, json):
        try:
            dao: MostHotelReservationsDAO = MostHotelReservationsDAO()
        except Exception:
            return jsonify("Server is not available"), 503

        result = dao.getMostHotelReservations()
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
            return jsonify("No valid results for Hotel Reservations"), 404
        else:
            result = list(
                map(
                    lambda x: MostHotelReservationsModel(hotel_name=x[0],
                                                  reservation_count=x[1]).
                    __dict__, result))
        return jsonify(result), 200