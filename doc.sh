#!/bin/sh

APP='realty-api'
CMD=$1

case $APP in
  "build")
    docker build -t $APP .
    ;;
  "run")
    docker run -d -p 80:80 --name $APP $APP
    ;;
  "start")
    docker start $APP
    ;;
  "stop")
    docker stop $APP
    ;;
  "attach")
    docker start -a $APP
    ;;
  "restart")
    docker restart $APP
    ;;
  "eject")
    docker rm $APP
    ;;
  "up-dev")
    docker compose -f docker-compose.dev.yml up --build
    ;;
  "up-prod")
    docker compose -f docker-compose.prod.yml up --build
    ;;
  "down")
    docker compose down
    ;;
  *)
    echo "Invalid command"
    echo "Usage: ./doc.sh [build|run|start|stop|attach|restart|eject|up-dev|up-prod|down]"
    ;;
esac
