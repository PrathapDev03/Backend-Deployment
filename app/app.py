from flask import Flask, request, jsonify
from faker import Faker
from models import db, Employee, Contact, Todo
from config import Config

fake = Faker()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return jsonify({
        "message": "Smart Office Backend Running"
    })


# ==========================
# EMPLOYEE CRUD
# ==========================

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


@app.route("/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])


@app.route("/employee/<int:id>", methods=["GET"])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict())


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


@app.route("/employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    return jsonify({"message": "Employee deleted"})


# ==========================
# CONTACT CRUD
# ==========================

@app.route("/contact", methods=["POST"])
def create_contact():
    data = request.json

    contact = Contact(
        name=data["name"],
        phone=data["phone"],
        email=data["email"]
    )

    db.session.add(contact)
    db.session.commit()

    return jsonify({"message": "Contact created"}), 201


@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([c.to_dict() for c in contacts])


# ==========================
# TODO CRUD
# ==========================

@app.route("/todo", methods=["POST"])
def create_todo():
    data = request.json

    todo = Todo(
        task=data["task"],
        status=data["status"]
    )

    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "Todo created"}), 201


@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([t.to_dict() for t in todos])


# ==========================
# AI DATA GENERATOR
# ==========================

@app.route("/generate-data", methods=["POST"])
def generate_data():

    employee = Employee(
        name=fake.name(),
        email=fake.email(),
        department=fake.job(),
        phone=fake.phone_number()
    )

    contact = Contact(
        name=fake.name(),
        phone=fake.phone_number(),
        email=fake.email()
    )

    todo = Todo(
        task=f"Complete {fake.job()} task",
        status="Pending"
    )

    db.session.add(employee)
    db.session.add(contact)
    db.session.add(todo)

    db.session.commit()

    return jsonify({
        "message": "AI Generated Data Created",
        "employee": employee.to_dict(),
        "contact": contact.to_dict(),
        "todo": todo.to_dict()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)