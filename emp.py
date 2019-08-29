from flask import Flask, request, flash, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/employees'

sql = SQLAlchemy(app)

marsh = Marshmallow(app)

class Employees(sql.Model):
   id = sql.Column('employe.id', sql.Integer, primary_key = True)
   name = sql.Column(sql.String(50))
   contact = sql.Column(sql.String(10))
   city = sql.Column(sql.String(50))

   def __init__(self, name, contact, city):
      self.name = name
      self.contact = contact
      self.city = city
      
class EmployeesSchema(marsh.Schema):
    class Meta:
      fields = ('id', 'name', 'contact', 'city')

employees_schema = EmployeesSchema()
employee_schema = EmployeesSchema(many=True)

@app.route('/', methods = ['GET'])
def get():
    total_employees = Employees.query.all()
    result = employee_schema.dump(total_employees).data
    return jsonify(result)

@app.route('/', methods = ['POST'])
def post():

    name = request.json['name']
    contact = request.json['contact']
    city = request.json['city']
    new_employee = Employees(name,contact,city)
    sql.session.add(new_employee)
    sql.session.commit()
    return ('success')

@app.route('/<id>', methods = ['PUT','GET','DELETE'])
def put(id):
    if request.method == 'PUT' :
        update = Employees.query.get(id)
        name = request.json['name']
        contact = request.json['contact']
        city = request.json['city']
        update.name=name
        update.contact=contact
        update.city=city
        sql.session.commit()
        return 'Details updated'
    
    if request.method == 'GET' :
        view = Employees.query.get(id)
        return employees_schema.jsonify(view)

    if request.method == 'DELETE' :
        delete = Employees.query.get(id)
        sql.session.delete(delete)
        sql.session.commit()
        return ('Deleted successfully')

if __name__ == '__main__':
   sql.create_all()
   app.run(debug = True)
