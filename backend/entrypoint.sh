#!/bin/bash

python manage.py migrate
python manage.py loaddata fixtures/Professions.json
python manage.py loaddata fixtures/Question.json
python manage.py loaddata fixtures/Chance.json
python manage.py loaddata fixtures/Answer.json
python manage.py runserver 0.0.0.0:8200
