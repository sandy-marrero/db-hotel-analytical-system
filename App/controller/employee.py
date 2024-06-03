from ETL.table_representations import EmployeeTableDataNoPK, EmployeeTableData
from model.employee import EmployeeDAO
from flask import jsonify

class Employee:
    def make_json(self, tuples) -> list:
        result = []
        for row in tuples:
            json_obj = {
                'eid': row[0],
                'hid': row[1],
                'fname': row[2],
                'lname': row[3],
                'age': row[4],
                'position': row[5],
                'salary': row[6]
            }
            result.append(json_obj)
        return result
    
    def getAll(self) -> list:
        try:
            model = EmployeeDAO()
        except Exception:
            return jsonify("Server unavailable"), 400
        employees = model.getAll()
        if employees is None:
            return jsonify("No employees found"), 404
        answer = self.make_json(employees)
        return answer
    
    def getById(self, id) -> list:
        try:
            model = EmployeeDAO()
        except Exception:
            return jsonify("Server unavailable"), 400
        employee = model.getById(id)
        if employee is None:
            return jsonify("Client not found"), 404
        answer = self.make_json([employee])
        return answer
    
    def updateEmployee(self, id, employee_data) -> int:
        try:
            employee = EmployeeTableData(eid=id, hid = employee_data.get("hid"), fname=employee_data.get("fname"), lname=employee_data.get('lname'), age=employee_data.get("age"), position=employee_data.get('position'), salary=employee_data.get('salary'))
            try:
                model = EmployeeDAO()
            except Exception:
                return jsonify("Server Unavailable"), 503
            updated_employee = model.update_Employee(id, employee.hid, 
                                               employee.fname, 
                                               employee.lname,
                                               employee.age,
                                               employee.position,
                                               employee.salary)
            if updated_employee is None:
                return jsonify("Employee not found"), 404
            else:
                return jsonify({"eid": int(updated_employee)}), 200
        except Exception:
            return jsonify("Invalid Request Body"), 400
    
    def createEmployee(self, employee_data) -> int:
        try:
            try:
                model = EmployeeDAO()
            except Exception:
                return jsonify("Server Unavailable"), 503
            employee = EmployeeTableDataNoPK(hid = employee_data.get("hid"), fname=employee_data.get("fname"), lname=employee_data.get('lname'), age=employee_data.get("age"), position=employee_data.get('position'), salary=employee_data.get('salary'))
            hid = employee.hid
            first_name = employee.fname
            last_name = employee.lname
            age = employee.age
            position = employee.position
            salary = employee.salary
            new_employee = model.create_Employee(hid, first_name, last_name, age, position, salary)
            return jsonify(new_employee)
        except Exception:
            return jsonify("Invalid Request Body"), 400
    
    def deleteEmployee(self, eid: int):
        try:
            try:
                model = EmployeeDAO()
            except Exception:
                return jsonify("Server Unavailable"),503
            eid = int(eid)
            deleted_employee = model.delete_Employee(eid)
            if deleted_employee is False:
                return jsonify(f"Employee {eid} was not deleted."), 404
            else:
                return jsonify({"eid": deleted_employee}), 200
        except Exception:
            return jsonify(f"Employee {eid} was not deleted."), 404
