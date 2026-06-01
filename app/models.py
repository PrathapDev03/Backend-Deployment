from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(db.Model):

    __tablename__ = "employees"

    employee_id = db.Column(
        db.Integer,
        primary_key=True
    )

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