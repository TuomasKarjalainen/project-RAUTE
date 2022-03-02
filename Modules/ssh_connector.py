import sys
import pymysql
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
from dotenv import load_dotenv
from os import getenv

  


class Connector(): #Pass the path to your env file when you call this class
    """
    --------------------------------------------------------
    VERSION 2021-12-09
    Latest updates
    - All variables are now taken from environment variables
    --------------------------------------------------------
    """
    
    def __init__(self, path): 
        
        load_dotenv(path)
        ssh = paramiko.SSHClient()  # Here we use paramiko library and its SSHClient function
        self.mypkey = ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Here we add a fingerprint
        self.sql_hostname = getenv("MARIADB_IP")
        self.sql_username = getenv("MARIADB_USER")
        self.sql_password = getenv("MARIADB_PASSWORD")
        self.sql_main_database = getenv("MARIADB_DATABASE")
        self.sql_port = int(getenv("MARIADB_PORT"))
        
        self.ssh_host = getenv("SSH_HOST")
        self.ssh_user = getenv("SSH_USER")
        self.ssh_port = int(getenv("SSH_PORT"))
        self.ssh_password = ssh_password = getenv("SSH_PASSWORD")  #Here we take our ssh credentials from the env file
        
    def connector(self, query):  # Here we use SSHTunnelForwarder from sshtunnel library to first make connection to the Blade
                                 # Also remember to pass query you want to run in the database
        with SSHTunnelForwarder(
        (self.ssh_host, self.ssh_port),
        ssh_username=self.ssh_user,
        ssh_pkey=self.mypkey,
        ssh_password=self.ssh_password,
        remote_bind_address=(self.sql_hostname, self.sql_port)) as tunnel:  #Here we just passed our ssh credentials and saved them as tunnel
            conn = pymysql.connect(host='localhost', user=self.sql_username, 
                passwd=self.sql_password, db=self.sql_main_database, #Credentials to our mariadb container and to our database 
                port=tunnel.local_bind_port)  # And finally here we connect to blade
            data = pd.read_sql_query(query, conn) # And here we pass the query
            conn.close()
        return data