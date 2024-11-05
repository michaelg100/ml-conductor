#!/bin/bash

IMAGE='mysql-image'
CONTAINER='mysql-container'


result=$(docker ps -a --format {{.Names}} | grep $CONTAINER)

if [[ -n "$result" ]]; then
    docker rm -f $CONTAINER
    echo "container deleted"
    docker rm -f $IMAGE
    echo "image removed"
fi


echo "run container"

docker build -t $IMAGE .

docker run -d -p 4001:3306 --name $CONTAINER \
    -v $(pwd):/app \
    -e MYSQL_ROOT_PASSWORD=password $IMAGE