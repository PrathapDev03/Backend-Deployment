class Config:

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://officeadmin:office-db-01@office-db-01.cbuoa8kc81xo.ap-southeast-1.rds.amazonaws.com:3306/office_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False