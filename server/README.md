1) Setup virtualenv

2) checkout code.

3) get dependencies

4) Do python manage.py makemigrations

 5) Do python manage.py migrate

6) Do python manage.py runserver


Run tests
python3 manage.py test 
python3 manage.py test displaycode.tests
python3 manage.py test displaycode.tests.TestRestAPI
python3 manage.py test displaycode.tests.TestRestAPI.testGetComments


Copy coding blindspot repo to static directory

Open following link in browser.
http://127.0.0.1:8000/static/dist/index.html


