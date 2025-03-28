#!/bin/bash

# Загрузка переменных окружения из .env файла
source .env

# Параметры подключения к PostgreSQL
DB_NAME="$DB_NAME"
DB_USER="$DB_USER_NM"
DB_PASSWORD="$DB_PASSWORD"
DB_HOST="$DB_IP"
DB_PORT="$DB_PORT"

# Создание базы данных
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME";

# Создание пользователя с паролем
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD'";

# Назначение прав пользователю на базу данных
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER";

echo "База данных, пользователь и права успешно созданы."