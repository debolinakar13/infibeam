#Infibeam

- create virtual environment

```
virtualenv -p python3 <name>
```
- run the following commands to map models and database

**Run Command**
```
python3 manage.py makemigrations

```
```
python3 manage.py migrate
```

```
python3 manage.py migrate --run-syncdb
```

- To run the django app use follwoing command:
**Run Command**
```
python3 manage.py runserver <port>
```
