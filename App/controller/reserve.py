"""Reserve table controller for term project - hotel analytics system."""
from model.reserve import ReserveDAO
from ETL.table_representations import ReserveTableData, ReserveTableDataNoPK
from flask import jsonify


class Reserve:
    """Controller from reserve table."""

    def getAllReservations() -> (str, int):
        """Get all reservations from ReserveDAO.

        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            dao = ReserveDAO()
        except Exception:
            return jsonify("Server is not available"), 503
        result = dao.getAllReservations()
        if result is None:
            return jsonify("No reservations found"), 404
        else:
            result = list(
                map(
                    lambda x: ReserveTableData(reid=x[0],
                                               ruid=x[1],
                                               clid=x[2],
                                               total_cost=x[3],
                                               payment=x[4],
                                               guests=x[5]).__dict__, result))
            return jsonify(result)

    def getReservationById(reid: int) -> (str, int):
        """Get reservation from ReserveDAO by primary key.

        :param reid: Primary for reserve table.
        :type reid: ``int``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            dao = ReserveDAO()
        except Exception:
            return jsonify("Server is not available"), 503
        result = dao.getReservationById(reid)
        if result is None:
            return jsonify(f"No reservation with ID {reid} was found."), 404
        else:
            result = ReserveTableData(reid=result[0],
                                      ruid=result[1],
                                      clid=result[2],
                                      total_cost=result[3],
                                      payment=result[4],
                                      guests=result[5]).__dict__
            return jsonify(result)

    def createReservation(json) -> (str, int):
        """Create reservation into ReserveDAO.

        :param json: JSON from flask request
        :type json: ``json``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            reservation: ReserveTableDataNoPK = ReserveTableDataNoPK(
                ruid=json.get('ruid'),
                clid=json.get('clid'),
                payment=json.get('payment'),
                guests=json.get('guests'))
            try:
                dao: ReserveDAO = ReserveDAO()
            except Exception:
                return jsonify("Server is not available"), 503
            result = dao.createReservation(reservation)
            if result is None:
                return jsonify("Reservation could not be created"), 500
            else:
                return jsonify({"reid": int(result)})
        except Exception:
            return jsonify("Invalid request body"), 400

    def updateReservation(reid: int, json: str) -> (str, int):
        """Create reservation into ReserveDAO.

        :param reid: Primary key from reservation table
        :type reid: ``int``
        :param json: JSON from flask request
        :type json: ``json``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            reservation: ReserveTableData = ReserveTableData(
                reid=reid,
                ruid=json.get('ruid'),
                clid=json.get('clid'),
                total_cost=json.get('total_cost'),
                payment=json.get('payment'),
                guests=json.get('guests'))
            try:
                dao: ReserveDAO = ReserveDAO()
            except Exception:
                return jsonify("Server is not available"), 503
            result = dao.updateReservation(reservation)
            if result is None:
                return jsonify("Reservation could not be updated"), 500
            else:
                return jsonify({"reid": int(result)})
        except Exception:
            return jsonify("Invalid request body"), 400

    def deleteReservation(reid: int):
        """Delete reserve into ReserveDAO.

        :param reid: Primary key from reserve table
        :type reid: ``int``
        :rtype: ``(str, int)`` A tuple with a json object and status code.
        """
        try:
            reid = int(reid)
            try:
                dao: ReserveDAO = ReserveDAO()
            except Exception:
                return jsonify("Server is not available"), 503
            if dao.deleteReservation(reid) is False:
                return jsonify(
                    f"Reservation with ID {reid} could not be deleted."), 404
            else:
                return jsonify(reid)
        except Exception:
            return jsonify(
                f"Reservation with ID {reid} could not be deleted."), 404
