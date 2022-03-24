#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python3 manage.py makemigrations shop
python3 manage.py makemigrations search
python3 manage.py makemigrations orders
python3 manage.py makemigrations loyalty_program
python3 manage.py makemigrations favorites
python3 manage.py makemigrations discount_system
python3 manage.py makemigrations cart
python3 manage.py makemigrations blog
python3 manage.py makemigrations account
python3 manage.py migrate



exec "$@"