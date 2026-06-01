from flask import Flask, request, jsonify
from faker import Faker

from models import db, Employee, Contact, Todo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

fake = Faker()

with app.app_context():
    db.create_all()


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Smart Office Management API Version 5" 
    })


# --------------------------------------------------
# EMPLOYEE CRUD
# --------------------------------------------------

@app.route("/employees", methods=["POST"])
def create_employee():

    data = request.get_json()

    employee = Employee(
        name=data["name"],
        email=data["email"],
        department=data["department"],
        designation=data["designation"],
        salary=data["salary"]
    )

    db.session.add(employee)
    db.session.commit()

    return jsonify({
        "message": "Employee Created Successfully"
    }), 201


@app.route("/employees", methods=["GET"])
def get_employees():

    employees = Employee.query.all()

    return jsonify(
        [emp.to_dict() for emp in employees]
    )


@app.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):

    employee = Employee.query.get_or_404(id)

    return jsonify(employee.to_dict())


@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):

    employee = Employee.query.get_or_404(id)

    data = request.get_json()

    employee.name = data.get("name", employee.name)
    employee.email = data.get("email", employee.email)
    employee.department = data.get("department", employee.department)
    employee.designation = data.get("designation", employee.designation)
    employee.salary = data.get("salary", employee.salary)

    db.session.commit()

    return jsonify({
        "message": "Employee Updated Successfully"
    })


@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    return jsonify({
        "message": "Employee Deleted Successfully"
    })


# --------------------------------------------------
# CONTACT CRUD
# --------------------------------------------------

@app.route("/contacts", methods=["POST"])
def create_contact():

    data = request.get_json()

    contact = Contact(
        name=data["name"],
        phone=data["phone"],
        email=data["email"]
    )

    db.session.add(contact)
    db.session.commit()

    return jsonify({
        "message": "Contact Created Successfully"
    }), 201


@app.route("/contacts", methods=["GET"])
def get_contacts():

    contacts = Contact.query.all()

    return jsonify(
        [c.to_dict() for c in contacts]
    )


# --------------------------------------------------
# TODO CRUD
# --------------------------------------------------

@app.route("/todos", methods=["POST"])
def create_todo():

    data = request.get_json()

    todo = Todo(
        task=data["task"],
        status=data["status"]
    )

    db.session.add(todo)
    db.session.commit()

    return jsonify({
        "message": "Todo Created Successfully"
    }), 201


@app.route("/todos", methods=["GET"])
def get_todos():

    todos = Todo.query.all()

    return jsonify(
        [t.to_dict() for t in todos]
    )


# --------------------------------------------------
# AI GENERATED DATA
# --------------------------------------------------

@app.route("/generate-data", methods=["POST"])
def generate_data():

    employee = Employee(
        name=fake.name(),
        email=fake.unique.email(),
        department="DevOps",
        designation="DevOps Engineer",
        salary=500000
    )

    contact = Contact(
        name=fake.name(),
        phone=fake.phone_number(),
        email=fake.email()
    )

    todo = Todo(
        task="Deploy Flask Application",
        status="Pending"
    )

    try:
        db.session.add(employee)
        db.session.add(contact)
        db.session.add(todo)

        db.session.commit()

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500

    return jsonify({
        "message": "AI Data Generated Successfully",
        "employee": employee.to_dict(),
        "contact": contact.to_dict(),
        "todo": todo.to_dict()
    })


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )