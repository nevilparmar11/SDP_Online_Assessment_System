release: sh -c 'cd ./onlineassessmentsystem/ && exec python manage.py migrate'
web: sh -c 'cd ./onlineassessmentsystem/ && exec gunicorn onlineassessmentsystem.wsgi --log-file -'
