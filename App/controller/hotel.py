from ETL.table_representations import HotelTableData, HotelTableDataNoPk
from model.hotel import HotelDAO
from flask import jsonify

class Hotel:
    def make_json(self, tuples) -> list:
        result = []
        for row in tuples:
            json_obj = {
                'hid': row[0],
                'chid': row[1],
                'hname': row[2],
                'hcity': row[3]
            }
            result.append(json_obj)
        return result
    
    def getAll(self) -> list:
        try:
            model = HotelDAO()
        except Exception:
            return jsonify("Server unavailable"), 503
        hotels = model.getAll()
        if hotels is None:
            return jsonify("No hotels found"), 404
        answer = self.make_json(hotels)
        return jsonify(answer)
        
    def getById(self, id) -> list:
        try:
            model = HotelDAO()
        except Exception:
            return jsonify("Server unavailable"), 503
        hotel = model.getById(id)
        if hotel is None:
            return jsonify("Hotel not found"), 404
        answer = self.make_json([hotel])
        return jsonify(answer)
    
    def createHotel(self, hotel_data) -> int:
        try:
            model = HotelDAO()
            try:
                hotel = HotelTableDataNoPk(chid=hotel_data.get("chid"), hname=hotel_data.get("hname"), hcity=hotel_data.get('hcity'))
            except Exception:
                return jsonify("Bad request."), 400
        except Exception:
            return jsonify("Server unavailable"), 503
        new_hotel = model.addHotel(hotel_data.get("chid"),hotel_data.get("hname"), hotel_data.get('hcity'))
        if new_hotel == False:
            return jsonify("Chid not in chains."), 404
        return jsonify(new_hotel)
    
    
    def updateHotel(self, id, hotel_data) -> int:
        try:
            model = HotelDAO()
            try:
                hotel = HotelTableData(hid=id, chid=hotel_data.get("chid"), hname=hotel_data.get('hname'), hcity=hotel_data.get('hcity'))
            except Exception:
                return jsonify("Bad request."), 400
        except Exception:
            return jsonify("Server unavailable"), 503
        updated_hotel = model.updateHotel(id=id, chid=hotel_data.get("chid"), hname=hotel_data.get('hname'), hcity=hotel_data.get('hcity'))
        if updated_hotel == False:
            return jsonify("Unable to update hotel."),400
        return jsonify(updated_hotel), 200
    
    def deleteHotel(self, hid: int):
        try:
            hid = int(hid)
            try:
                dao: HotelDAO = HotelDAO()
            except Exception:
                return jsonify("Server is not available"), 503
            if dao.deleteHotel(hid) is False:
                return jsonify(
                    f"Hotel with ID {hid} could not be deleted."), 404
            else:
                return jsonify(hid)
        except Exception:
            return jsonify(
                f"Hotel with ID {hid} could not be deleted."), 404