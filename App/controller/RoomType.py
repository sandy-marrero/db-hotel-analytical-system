from model.RoomType import RoomTypeDAO
from ETL.aggregate_representations import RoomTypeModel
from flask import jsonify

class RoomType:

    def getRoomType(hid: int, json) -> (str, int):
        try:
            dao: RoomTypeDAO = RoomTypeDAO()
        except Exception:
            return jsonify("Server is not available"), 503
        
        try:
            eid = int(json.get("eid"))
        except Exception:
            return jsonify("Invalid Request Body"), 400
        
        if dao.conn.isAuthorizedEmployee(hid, json.get("eid")) == False:
            return jsonify("Unauthorized user"), 403
            
        result = dao.getRoomTypeDAO(hid)
        if result is None:
            return jsonify(f"No hotel with ID {hid} was found"), 404
        else:
            result = list(
                map(
                    lambda x: RoomTypeModel(room_type=x[0],
                                                  total_reservations=x[1]).
                    __dict__, result))
        return jsonify(result), 200