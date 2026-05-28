from flask import Flask, request, jsonify
from models import db, Employee
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Smart Office Backend Running"})


# CREATE Employee
@app.route("/employee", methods=["POST"])
def create_employee():
    data = request.json

    employee = Employee(
        name=data["name"],
        email=data["email"],
        department=data["department"],
        phone=data["phone"]
    )

    db.session.add(employee)
    db.session.commit()

    return jsonify({"message": "Employee created"}), 201


# GET All Employees
@app.route("/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])


# GET Single Employee
@app.route("/employee/<int:id>", methods=["GET"])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict())


# UPDATE Employee
@app.route("/employee/<int:id>", methods=["PUT"])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.json

    employee.name = data.get("name", employee.name)
    employee.email = data.get("email", employee.email)
    employee.department = data.get("department", employee.department)
    employee.phone = data.get("phone", employee.phone)

    db.session.commit()

    return jsonify({"message": "Employee updated"})


# DELETE Employee
@app.route("/employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    return jsonify({"message": "Employee deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)