#!/bin/bash
cd db
docker build -t db_image .
cd ..
docker-compose up --build
