from sqlalchemy import create_engine
import pandas as pd
import mysql.connector


def connection(host, user, password, database, port):
    sql_hostname = host
    sql_username = user
    sql_password = password
    sql_main_database = database
    sql_port = port

    db = mysql.connector.connect(
        host = host,
        user = user,
        passwd = password,
        database = database
        )


    engine =create_engine("mysql+pymysql://%s:%s@%s:%s/%s" % (sql_username, sql_password, sql_hostname, sql_port, sql_main_database))
    connection = engine.connect()
    return connection, db

def chunks(l, n):
# Yield successive n-sized chunks from l.

    for i in range(0, len(l), n):
         yield l.iloc[i:i+n]
        

def write_to_db(frame, engine, table_name, chunk_size):
    for idx, chunk in enumerate(chunks(frame, chunk_size)):
        chunk.to_sql(name=table_name, con=engine, if_exists='append', index = False)
