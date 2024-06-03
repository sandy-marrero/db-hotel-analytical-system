from ETL.table_representations import RoomDescriptionTableData, RoomDescriptionTableDataNoPK
from model.roomdescription import RoomDescriptionDAO
from flask import jsonify

class RoomDescription:
    def make_json(self, tuples) -> list:
        result = []
        for row in tuples:
            json_obj = {
                'rdid': row[0],
                'rname': row[1],
                'rtype': row[2],
                'capacity': row[3],
                'ishandicap': row[4]
            }
            result.append(json_obj)
        return result
    
    def getAll(self) -> list:
        try:
            model = RoomDescriptionDAO()
        except Exception:
            return jsonify("Server unavailable"), 503
        roomdetails = model.getAll()
        if roomdetails is None:
            return jsonify("No room details found"), 404
        answer = self.make_json(roomdetails)
        return answer
    
    def getById(self, id) -> list:
        try:
            model = RoomDescriptionDAO()
        except Exception:
            return jsonify("Server unavailable"), 503
        roomdetail = model.getById(id)
        if roomdetail is None:
            return jsonify("Room description not found"), 404
        answer = self.make_json([roomdetail])
        return answer
    
    def updateRoomDescription(self, id: int, roomDescription_data: str) -> (str, int):
        try:
            room_description = RoomDescriptionTableData(rdid=id, rname=roomDescription_data.get("rname"), rtype=roomDescription_data.get('rtype'), capacity=roomDescription_data.get("capacity"), ishandicap=bool(roomDescription_data.get('ishandicap')))
            try:
                model = RoomDescriptionDAO()
            except Exception:
                return jsonify("Server Unavailable"), 503
            updated_roomDescription = model.update_roomDescription(id, room_description.rname,
                                                      room_description.rtype,
                                                      room_description.capacity,
                                                      room_description.ishandicap)
            if updated_roomDescription is None:
                return jsonify("Room Description not found"), 404
            else:
                return jsonify({"rdid": int(updated_roomDescription)}), 200
        except Exception:
            return jsonify("Invalid Request Body"), 400
    
    def createRoomDescription(self, roomDescription_data) -> int:
        try:
            try:
                model = RoomDescriptionDAO()
            except Exception:
                return jsonify("Server Unavailable"), 503
            roomDescription = RoomDescriptionTableDataNoPK(rname=roomDescription_data.get("rname"), rtype=roomDescription_data.get('rtype'), capacity=roomDescription_data.get("capacity"), ishandicap=bool(roomDescription_data.get('ishandicap')))
            room_name = roomDescription.rname
            room_type = roomDescription.rtype
            capacity = roomDescription.capacity
            ishandicap = roomDescription.ishandicap
            new_roomDescription = model.create_roomDescription(room_name, room_type, int(capacity), ishandicap)
            return jsonify({"rdid": new_roomDescription})
        except Exception:
            return jsonify("Invalid Request Body"), 400
    
    def delete_roomDescription(self, rdid: int) -> int:
        try:
            rdid = int(rdid)
            try:
                model = RoomDescriptionDAO()
            except Exception:
                return jsonify("Server Unavailable"),503
            deleted_roomDescription = model.delete_roomRescription(rdid)
            if deleted_roomDescription is False:
                return jsonify(f"Room Description {rdid} was not deleted."), 404
            else:
                return jsonify(deleted_roomDescription), 200
        except Exception:
            return jsonify(f"Room Description {rdid} was not deleted."), 404

