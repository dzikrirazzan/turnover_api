web: DJANGO_SETTINGS_MODULE=backend.turnover_prediction.settings PYTHONPATH=$PYTHONPATH:./backend gunicorn --worker-tmp-dir /dev/shm backend.turnover_prediction.wsgi:application
release: python run_migrations.py && DJANGO_SETTINGS_MODULE=backend.turnover_prediction.settings PYTHONPATH=$PYTHONPATH:./backend python backend/manage.py fix_production_db --skip-test
