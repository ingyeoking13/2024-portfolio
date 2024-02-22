docker rm -f redis 2> /dev/null
docker run --name redis -p 6379:6379 -d redis