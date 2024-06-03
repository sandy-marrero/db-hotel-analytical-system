from flask import jsonify
from ETL.table_representations import ChainsTableDataNoPK, ChainsTableData
from model.chain import ChainsDAO

class Chain:
    def make_json(self, tuples) -> list:
        result = []
        for row in tuples:
            json_obj = {
                'chid': row[0],
                'name': row[1],
                'springmkup': row[2],
                'summermkup': row[3],
                'fallmkup': row[4],
                'wintermkup': row[5]
            }
            result.append(json_obj)
        return result
    def getAll(self) -> list:
        try:
            model = ChainsDAO()
        except Exception:
            return jsonify("Server Unavailable"), 503
        chains = model.getAll()
        if chains is None:
            return jsonify("No Chains have been found on Database."), 404
        answer = self.make_json(chains)
        return jsonify(answer)
    
    def getById(self, id) -> list:
        try:
            model = ChainsDAO()
        except Exception:
            return jsonify("Server Unavailable"),503
        chain = model.getById(id)
        if chain is None:
            return jsonify(f"Chain with chid {id} has not been found."), 404
        answer = self.make_json([chain])
        return jsonify(answer)
    def createChain(self, chain_data) -> int:
        try:
            try:
                model = ChainsDAO()
            except Exception:
                return jsonify("Server Unavailable"), 503
            chain = ChainsTableDataNoPK(cname=chain_data.get("cname"), springmkup=chain_data.get('springmkup'), summermkup=chain_data.get('summermkup'), fallmkup=chain_data.get('fallmkup'), wintermkup=chain_data.get('wintermkup'))
            new_chain = model.addChain(chain_data.get("cname"), chain_data.get('springmkup'), chain_data.get('summermkup'), chain_data.get('fallmkup'), chain_data.get('wintermkup'))
            return jsonify({"chid": new_chain}),200
        except Exception:
            return jsonify("Invalid Request Body"), 400
    def updateChain(self, id, chain_data) -> int:
        try:
            chain = ChainsTableData(chid=id, cname=chain_data.get("cname"), springmkup=chain_data.get('springmkup'), summermkup=chain_data.get('summermkup'), fallmkup=chain_data.get('fallmkup'), wintermkup=chain_data.get('wintermkup'))
            try:
                model = ChainsDAO()
            except Exception:
                return jsonify("Server Unavailable"), 503
            updated_chain = model.updateChain(id, chain_data.get("cname"), chain_data.get('springmkup'), chain_data.get('summermkup'), chain_data.get('fallmkup'), chain_data.get('wintermkup'))
            if updated_chain is None:
                return jsonify("Chain not found"), 404
            else:
                return jsonify({"chid": int(updated_chain)}), 200
        except Exception:
            return jsonify("Invalid Request Body"), 400
    def deleteChain(self, id) -> int:
        try:
            try:
                model = ChainsDAO()
            except Exception:
                return jsonify("Server Unavailable"),503
            chid = int(id)
            deleted_chain = model.deleteChain(chid)
            if deleted_chain is False:
                return jsonify(f"Chain {chid} was not deleted."), 404
            else:
                return jsonify({"chid":chid}), 200
        except Exception:
            return jsonify(f"Chain {chid} was not deleted."), 404