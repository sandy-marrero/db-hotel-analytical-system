from ETL.table_representations import ClientTableDataNoPK, ClientTableData
from model.client import ClientDAO
from flask import jsonify
class Client:
    def make_json(self, tuples) -> list:
        result = []
        for row in tuples:
            json_obj = {
                'clid': row[0],
                'fname': row[1],
                'lname': row[2],
                'age': row[3],
                'memberyear': row[4]
            }
            result.append(json_obj)
        return result
    
    def getAll(self) -> list:
        try:
            model = ClientDAO()
        except Exception:
            return jsonify("Server unavailable"), 400
        clients = model.getAll()
        if clients is None:
            return jsonify("No clients found"), 404
        answer = self.make_json(clients)
        return jsonify(answer)
    
    def getById(self, id) -> list:
        try:
            model = ClientDAO()
        except Exception:
            return jsonify("Server unavailable"), 400
        client = model.getById(id)
        if client is None:
            return jsonify("Client not found"), 404
        answer = self.make_json([client])
        return jsonify(answer)
    
    
    def createClient(self, client_data) -> int:
        try:
            model = ClientDAO()
            try:
                client = ClientTableDataNoPK(fname=client_data.get("fname"), lname=client_data.get('lname'), age=client_data.get("age"), memberyear=client_data.get('memberyear'))
            except Exception:
                return jsonify("Bad request."), 400
        except Exception:
            return jsonify("Server unavailable"), 503
        new_client = model.addClient(client_data['fname'], client_data['lname'], client_data['age'], client_data['memberyear'])
        return jsonify(new_client)
    
    def updateClient(self, id, client_data) -> int:
        try:
            model = ClientDAO()
            try:
                client = ClientTableData(clid=id, fname=client_data.get("fname"), lname=client_data.get('lname'), age=client_data.get("age"), memberyear=client_data.get('memberyear'))
            except Exception:
                return jsonify("Bad request."), 400
        except Exception:
            return jsonify("Server unavailable"), 400
        updated_client = model.updateClient(id, fname=client_data.get("fname"), lname=client_data.get('lname'), age=client_data.get("age"), memberyear=client_data.get('memberyear'))
        if updated_client == False:
            return jsonify("Unable to update client"), 400
        return jsonify(updated_client), 200
    
    def deleteClient(self,clid: int):
        try:
            clid = int(clid)
            try:
                dao: ClientDAO = ClientDAO()
            except Exception:
                return jsonify("Server is not available"), 503
            if dao.deleteClient(clid) is False:
                return jsonify(
                    f"Client with ID {clid} could not be deleted."), 404
            else:
                return jsonify(clid)
        except Exception:
            return jsonify(
                f"Client with ID {clid} could not be deleted."), 404
    
