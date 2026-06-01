import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://officeadmin:Office@123@localhost/office_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False