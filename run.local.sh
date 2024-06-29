#!/bin/bash
# a script to execute the docker compose exec app bash and db bash command for docker compose file in the current directory
# usage: ./exec.sh [app|db|build]

if [ -z "$1" ]; then
  docker-compose -f docker-compose.local.yml up
fi

if [ "$1" == "app" ]; then
  docker-compose -f docker-compose.local.yml exec app bash
elif [ "$1" == "db" ]; then
  docker-compose -f docker-compose.local.yml exec db bash
elif [ "$1" == "build" ]; then
  docker-compose -f docker-compose.local.yml up --build
else
  echo "usage: exec.sh [app|db|build]"
  exit 1
fi

exit 0
