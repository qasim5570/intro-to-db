#!/bin/bash

# Backend structure
mkdir -p backend/app/models
mkdir -p backend/app/schemas
mkdir -p backend/app/routers
mkdir -p backend/app/db
mkdir -p backend/app/services
mkdir -p backend/scripts

# Frontend placeholder
mkdir -p frontend

# Docs structure
mkdir -p docs/report

touch backend/app/main.py
touch backend/app/db/postgres.py
touch backend/app/db/mongo.py
touch backend/requirements.txt
touch backend/.env.example
touch README.md

echo "Project structure created successfully."
