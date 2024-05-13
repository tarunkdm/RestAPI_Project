import pyodbc
import json
from flask import Response
from flask import jsonify
from flask import make_response
class user_model():
    def __init__(self):
        server = 'MSI'  # If SQL Server is on the same machine
        database = 'master'  # Replace 'YourDatabaseName' with your actual database name
        username = 'sa'  # Replace 'your_username' with your SQL Server username
        password = 'Trun$@$@4242'  # Replace 'your_password' with your SQL Server password

        # Create connection string
        try:
            self.conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
            self.conn = pyodbc.connect(self.conn_str)
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
            
            print("SQL Server Connection Successful")

        except:
            print("Error in Connecting SQL Server")

    def user_getall_model(self):
        query = 'select * FROM emp where emp_id = 2'
        self.cur.execute(query)
        temp  = self.cur.fetchall()
        result ={}
        for row in temp:
            result[row[0]] = row[1:]

        if len(result)>0:
            return make_response({"payload": result},200)
        else:
            return make_response({"message":"No Data Found"},204)

    def user_addone_model(self,data):
        self.cur.execute (f"INSERT INTO Emp (emp_id,emp_name, dep_id, salary, manager_id, emp_age, dept_name, gender) VALUES ('{data['ID']}','{data['Name']}','{data['Dept_id']}','{data['Salary']}','{data['manager_id']}','{data['emp_age']}','{data['dept_name']}', '{data['gender']}')")
        return make_response({"message":'User Added successfully'},201)

    def user_update_model(self,data):
        self.cur.execute (f"UPDATE emp SET emp_name = '{data['Name']}', salary = '{data['Salary']}', emp_age = '{data['age']}' WHERE emp_id =  {data['id']} ")
        if self.cur.rowcount >0:
            return make_response({"message":'User Updated successfully'},201)
        else:
            return make_response({"message":'Nothing to update'},202)

    def user_delete_model(self,id):
        self.cur.execute (f"DELETE FROM emp WHERE emp_id ={id}")
        if self.cur.rowcount >0:
            return make_response({"message":"User Deleted Successfully"},200)
        else:
            return make_response({"message":'Nothing to delete'},204)

    def user_patch_model(self,data,id):
        print(data)
        qry = "UPDATE emp SET "

        for key in data:
            qry =  qry + f"{key}='{data[key]}'" + ', '

        final_qry = qry[:-2] + f" WHERE emp_id = {id}"
        self.cur.execute(final_qry)

        if self.cur.rowcount >0:
            return make_response({"message":'User Updated successfully'},201)
        else:
            return make_response({"message":'Nothing to update'},202)



    def user_pagination_model(self, limit, page):
        limit = int(limit)
        page = int(page)
        qry = f"Select * FROM emp ORDER BY emp_id OFFSET {limit*(page-1)} ROWS FETCH NEXT {limit} ROWS ONLY"
        self.cur.execute(qry)
        temp = self.cur.fetchall()
        result = {}
        for row in temp:
            result[row[0]] = row[1:]
            
        if len(result)>0:
            return make_response({"payload": result},200)
        else:
            return make_response({"message":"No Data Found"},204)


