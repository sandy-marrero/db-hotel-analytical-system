from model.login import LoginDAO
from ETL.table_representations import LoginTableDataNoPK, LoginTableData
from flask import jsonify

class Login:
    def make_json(self, tuples) -> list:
        result = []
        for row in tuples:
            json_obj = {
                'lid': row[0],
                'eid': row[1],
                'user': row[2],
                'pass': row[3]
            }
            result.append(json_obj)
        return result
    
    def getAll(self) -> list:
        try:
            model = LoginDAO()
        except Exception:
            return jsonify("Server Unavailable"), 503
        logins = model.getAll()
        if logins is None:
            return jsonify("No logins found"), 404
        answer = self.make_json(logins)
        return jsonify(answer)
    
    def getById(self, id) -> list:
        try:
            model = LoginDAO()
        except Exception:
            return jsonify("Server Unavailable"), 503
        login = model.getById(id)
        if login is None:
            return jsonify("Login not found"), 404
        answer = self.make_json([login])
        return jsonify(answer)
    
    def updateLogin(self, id : int, login_data: str) -> (str, int):
        try:
            login = LoginTableData(lid = id, eid=login_data.get('eid'), username=login_data.get('username'), password=login_data.get('password'))
            try:
                model = LoginDAO()
            except Exception:
                return jsonify("Server Unavailable"), 503
            updated_id = model.update_login(id, login.eid, login.username, login.password)
            if updated_id is None:
                return jsonify("Login not found"), 404
            elif updated_id is False:
                return jsonify("Login for that eid already exists"), 409
            else:
                return jsonify({"lid": int(updated_id)})
        except Exception:
            return jsonify("Invalid Request Body"), 400
    
    def createLogin(self, login_data) -> int:
        try:
            model = LoginDAO()
            
            login = LoginTableDataNoPK(eid=login_data.get('eid'), username=login_data.get('username'), password=login_data.get('password'))
        except Exception:
            return jsonify("Invalid Request Body"), 400
        new_id = model.create_login(login.eid, login.username, login.password)
        if new_id is False:
            return jsonify("Login for that eid already exists"), 409
        return jsonify({"lid": new_id}), 200
    
    def deleteLogin(self, id) -> int:
        try:
            try:
                model = LoginDAO()
            except Exception:
                return jsonify("Server Unavailable"), 503
            lid = int(id)
            result = model.delete_login(id)
            if result is False:
                return jsonify(f"Login {lid} was not deleted."), 404
            else:
                return jsonify({"lid": lid}),200
        except Exception:
            return jsonify(f"Login {lid} was not deleted."), 404