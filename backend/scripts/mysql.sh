docker rm -f mysql 2> /dev/null
docker run --name mysql -e MYSQL_ROOT_PASSWORD=adkb -p 3306:3306 -d mysql:8.0