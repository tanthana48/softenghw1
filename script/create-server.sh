#!/bin/bash

# If no args, return usage
if [ $# -lt 1 ]; then
	echo "Usage: ./create-server.sh {password}"
	exit
fi


docker run --name mysql-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=$1 -d mysql
while ! docker exec -i mysql-db mysql --user=root --password=$1 -e "status" &> /dev/null ; do
    echo "Waiting for database to start..."
    sleep 2
done
docker exec -i mysql-db mysql -u root -p$1 < ./scripts/create-table.sql

echo "Server created sucessfully"
