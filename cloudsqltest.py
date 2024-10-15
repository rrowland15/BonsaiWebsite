# ~VD6kQL]nUT9fuiO
# bambam
# 34.127.33.7
# sage-wave-438701-h2:us-west1:bambam
#
# 50.35.182.31
# root
# ;]uAdsIdUTkyi,>P

# import os
# credential_path = "credentials.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
#
#
# import mysql.connector
#
# #connection = mysql.connector.connect(user='root',password=';]uAdsIdUTkyi,>P',host='34.127.33.7',database="treeusers")
# connection = mysql.connector.connect(user='bambam',password='~VD6kQL]nUT9fuiO',host='34.127.33.7',database="treeusers")
# cursor = connection.cursor()
# query1 = ("select * from users")
# cursor.execute(query1)
# print(cursor.fetchall())
# print("here")

import os
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import sqlalchemy

credential_path = "credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of MySQL.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = 'sage-wave-438701-h2:us-west1:bambam'  # e.g. 'project:region:instance'
    db_user = 'bambam'  # e.g. 'my-db-user'
    db_pass = '~VD6kQL]nUT9fuiO'  # e.g. 'my-db-password'
    db_name = "treeusers"  # e.g. 'my-database'

    ip_type = IPTypes.PUBLIC# IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
    print(ip_type)
    connector = Connector(ip_type)



    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            'sage-wave-438701-h2:us-west1:bambam',
            "pymysql",
            user='bambam',
            password='~VD6kQL]nUT9fuiO',
            db="treeusers",
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
        # ...
    )
    return pool


pool= connect_with_connector()

# insert statement
insert_stmt = sqlalchemy.text(
    "INSERT INTO users (user, image,text) VALUES (:user, :image,:text)",
)

with pool.connect() as db_conn:
    # insert into database
    db_conn.execute(insert_stmt, parameters={"user": "brutus", "image": "'boba.jpg'","text":"boba_tea"})


    # query database
    result = db_conn.execute(sqlalchemy.text("SELECT * from users")).fetchall()

    # commit transaction (SQLAlchemy v2.X.X is commit as you go)
    db_conn.commit()

    # Do something with the results
    for row in result:
        print(row)