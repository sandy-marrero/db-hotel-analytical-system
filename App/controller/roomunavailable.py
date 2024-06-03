from model.roomunavailable import RoomUnavailableDAO
from ETL.table_representations import RoomUnavailableTableDataNoPK, RoomUnavailableTableData

from flask import jsonify

class RoomUnavailable:
    def make_json(self, tuples) -> list:
        result = []
        for row in tuples:
            json_obj = {
                'ruid': row[0],
                'rid': row[1],
                'startdate': row[2],
                'enddate': row[3]
            }
            result.append(json_obj)
        return result
    
    def getAll(self) -> list:
        try:
            model = RoomUnavailableDAO()
        except Exception:
            return jsonify("Server unavailable"), 400
        roomunavailables = model.getAll()
        if roomunavailables is None:
            return jsonify("No roomunavailables found"), 404
        answer = self.make_json(roomunavailables)
        return jsonify(answer)
    
    
    def getById(self, id) -> list:
        try:
            model = RoomUnavailableDAO()
        except Exception:
            return jsonify("Server unavailable"), 400
        roomunavailable = model.getById(id)
        if roomunavailable is None:
            return jsonify("Room unavailable not found"), 404
        answer = self.make_json([roomunavailable])
        return jsonify(answer)
    
    
    def createRoomUnavailable(self, roomunavailable_data) -> int:
        try:
            model = RoomUnavailableDAO()
            try:
                roomunavailable = RoomUnavailableTableDataNoPK(rid=roomunavailable_data.get("rid"),startdate=roomunavailable_data.get("startdate"), enddate=roomunavailable_data.get('enddate'))
            except Exception:
                return jsonify("Bad request."), 400
        except Exception:
            return jsonify("Server unavailable"), 503
        new_roomunavailable = model.addRoomUnavailable(roomunavailable_data['rid'], roomunavailable_data['startdate'], roomunavailable_data['enddate'])
        if new_roomunavailable == False:
            return jsonify("rid is not in database."), 404
        return jsonify(new_roomunavailable)
    
    def updateRoomUnavailable(self, id, roomunavailable_data) -> int:
        try:
            model = RoomUnavailableDAO()
            try:
                roomunavailable = RoomUnavailableTableData(ruid=id, rid=roomunavailable_data.get("rid"),startdate=roomunavailable_data.get("startdate"), enddate=roomunavailable_data.get('enddate'))
            except Exception:
                return jsonify("Bad request."), 400
        except Exception:
            return jsonify("Server unavailable"), 503
        updated_roomunavailable = model.updateRoomUnavailable(id=id, rid=roomunavailable_data.get("rid"),startdate=roomunavailable_data.get("startdate"), enddate=roomunavailable_data.get('enddate'))
        if updated_roomunavailable is False:
            return jsonify("Either rid or ruid not in database."), 404
        return jsonify(updated_roomunavailable), 200
    
    def deleteRoomUnavailable(self, ruid: int):
        try:
            ruid = int(ruid)
            try:
                dao: RoomUnavailableDAO = RoomUnavailableDAO()
            except Exception:
                return jsonify("Server is not available"), 503
            if dao.deleteRoomUnavailable(ruid) is False:
                return jsonify(
                    f"RoomUnavailable with ID {ruid} could not be deleted."), 404
            else:
                return jsonify(ruid)
        except Exception:
            return jsonify(
                f"RoomUnavailable with ID {ruid} could not be deleted."), 404
    