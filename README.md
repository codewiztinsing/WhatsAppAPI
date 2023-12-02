**Chat api server **

# Project Setup Guide

- create your working path and initiate your virtual environment
- after that you may follow as below

# Ashewa E-commerce Backend

## Python version

## Python 3.8.5

## Install Project

### Setup Postgres Database (just the first time)

```
$ sudo su postgres -c psql

postgres$ CREATE USER test_user WITH PASSWORD 'test_password';
postgres$ CREATE DATABASE chat_db OWNER test_password ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE template0;
postgres$ GRANT ALL PRIVILEGES ON DATABASE chat_db TO test_user;
postgres$ GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO test_user;
postgres$ ALTER USER test_user CREATEDB;
postgres$ ALTER ROLE test_user SUPERUSER;
postgres$ \q

```

### Create a virtualenv (just the first time)

    $ python3 -m venv venv

### Install requirements

Just the first time

    $ pip install -r requirements.txt

Other times

    $ pip-sync

### Setting up environment variables for project

Copy `.env_example` to `.env` file

### Migrate

    $ python3 manage.py migrate


# Run project

## Run the project

    $ python3 manage.py runserver

## Documentation



