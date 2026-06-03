import json
import boto3
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("employees-1")


def lambda_handler(event, context):

    http_method = event.get("httpMethod")
    path_params = event.get("pathParameters")

    # CREATE EMPLOYEE
    if http_method == "POST":

        body = json.loads(event["body"])

        employee = {
            "employee_id": str(uuid.uuid4()),
            "name": body["name"],
            "email": body["email"],
            "department": body["department"],
            "designation": body["designation"],
            "salary": str(body["salary"])
        }

        table.put_item(Item=employee)

        return {
            "statusCode": 201,
            "body": json.dumps(employee)
        }

    # GET ALL EMPLOYEES
    elif http_method == "GET" and not path_params:

        response = table.scan()

        return {
            "statusCode": 200,
            "body": json.dumps(response.get("Items", []))
        }

    # GET EMPLOYEE BY ID
    elif http_method == "GET" and path_params:

        employee_id = path_params["employee_id"]

        response = table.get_item(
            Key={
                "employee_id": employee_id
            }
        )

        employee = response.get("Item")

        if not employee:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "Employee Not Found"
                })
            }

        return {
            "statusCode": 200,
            "body": json.dumps(employee)
        }

    # UPDATE EMPLOYEE
    elif http_method == "PUT":

        employee_id = path_params["employee_id"]
        body = json.loads(event["body"])

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
                ":n": body["name"],
                ":e": body["email"],
                ":d": body["department"],
                ":des": body["designation"],
                ":s": str(body["salary"])
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Employee Updated Successfully"
            })
        }

    # DELETE EMPLOYEE
    elif http_method == "DELETE":

        employee_id = path_params["employee_id"]

        table.delete_item(
            Key={
                "employee_id": employee_id
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Employee Deleted Successfully"
            })
        }

    return {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Invalid Request"
        })
    }