# app/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(db.Model):

    __tablename__ = "employees"

    employee_id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    designation = db.Column(
        db.String(100),
        nullable=False
    )

    salary = db.Column(
        db.Integer,
        nullable=False
    )

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "designation": self.designation,
            "salary": self.salary
        }


class Contact(db.Model):

    __tablename__ = "contacts"

    contact_id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    email = db.Column(
        db.String(100)
    )

    def to_dict(self):
        return {
            "contact_id": self.contact_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }


class Todo(db.Model):

    __tablename__ = "todos"

    todo_id = db.Column(
        db.Integer,
        primary_key=True
    )

    task = db.Column(
        db.String(255),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    def to_dict(self):
        return {
            "todo_id": self.todo_id,
            "task": self.task,
            "status": self.status
        }