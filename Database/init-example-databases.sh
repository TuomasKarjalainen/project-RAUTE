#!/bin/bash

RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MariaDB service startup"
    sleep 5
    mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "status" > /dev/null 2>&1
    RET=$?
done

echo "Checking for databases to import from environment variables INSTALL_Projekti";

if [ -n "$Projekti" ]; then
    echo "=> Importing example database 'Projekti'"
    unzip /home/setup.sql.zip
    mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE Projekti;"
    mysql -uroot -p${MYSQL_ROOT_PASSWORD} Projekti < setup.sql
fi
