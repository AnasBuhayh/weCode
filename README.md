# weCode
The source code of WeCode.ly blog

# Specifications
- Framework: Django
- Database: PostgreSQL

# Installation

### Local database setup

- Create new Postgres database

### Development database setup

- Please email me at anas.buhayh@gmail.com if you would like to connect to the live database

### App Setup

- Clone the project to your preferred directory

`https://github.com/AnasBuhayh/weCode.git`

- Chenge the database variables to your newly created ones in the settings.py file

```
NAME = '[database name]'
USER = '[database user]'
PASSWORD = '[database password]'
HOST = 'localhost'
PORT = '5432'
```

- *Recomended:* Create a virtual environment

`python -m venv [env-name]`

- *Recomended:* Run virtual environment

`.\[env-name]\Scripts\activate`

- Install requirements

`pip install -r .\requirements.txt`

- ~~Comment the line below from  weCode/urls.py (To avoid migration complicatoins)~~

~~`path('', include('blog.urls')),`~~

- Make migrations

`python manage.py makemigrations`

then

`python manage.py migrate`

- ~~Uncomment the app link from weCode/urls.py~~

~~`path('', include('blog.urls')),`~~

- Create superuser

`python manage.py createsuperuser`

- Run application

`python ./manage.py runserver`
