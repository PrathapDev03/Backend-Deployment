from flask import Flask, request, jsonify
import boto3
import uuid

app = Flask(__name__)

dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-southeast-1"
)

table = dynamodb.Table("employees")


@app.route("/")
def home():
    return jsonify({
        "message": "ECS + DynamoDB Backend Running"
    })


# CREATE EMPLOYEE
@app.route("/employees", methods=["POST"])
def create_employee():

    data = request.get_json()

    employee = {
        "employee_id": str(uuid.uuid4()),
        "name": data["name"],
        "email": data["email"],
        "department": data["department"],
        "designation": data["designation"],
        "salary": str(data["salary"])
    }

    table.put_item(Item=employee)

    return jsonify({
        "message": "Employee Created Successfully",
        "employee": employee
    }), 201


# GET ALL EMPLOYEES
@app.route("/employees", methods=["GET"])
def get_employees():

    response = table.scan()

    return jsonify(response.get("Items", []))


# GET EMPLOYEE BY ID
@app.route("/employees/<employee_id>", methods=["GET"])
def get_employee(employee_id):

    response = table.get_item(
        Key={
            "employee_id": employee_id
        }
    )

    employee = response.get("Item")

    if not employee:
        return jsonify({
            "message": "Employee Not Found"
        }), 404

    return jsonify(employee)


# UPDATE EMPLOYEE
@app.route("/employees/<employee_id>", methods=["PUT"])
def update_employee(employee_id):

    data = request.get_json()

    table.update_item(
        Key={
            "employee_id": employee_id
        },
        UpdateExpression="""
            SET #n=:n,
                email=:e,
                department=:d,
                designation=:des,
                salary=:s
        """,
        ExpressionAttributeNames={
            "#n": "name"
        },
        ExpressionAttributeValues={
            ":n": data["name"],
            ":e": data["email"],
            ":d": data["department"],
            ":des": data["designation"],
            ":s": str(data["salary"])
        }
    )

    return jsonify({
        "message": "Employee Updated Successfully"
    })


# DELETE EMPLOYEE
@app.route("/employees/<employee_id>", methods=["DELETE"])
def delete_employee(employee_id):

    table.delete_item(
        Key={
            "employee_id": employee_id
        }
    )

    return jsonify({
        "message": "Employee Deleted Successfully"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )