docker rm -f nginx 2> /dev/null
docker run --name nginx -p 80:80 -d nginx:latest
docker cp default.conf nginx:/etc/nginx/conf.d