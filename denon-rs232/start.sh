#!/usr/bin/env bash

docker-compose up -d
docker logs -f avr_test
