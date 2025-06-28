web: cd backend && python manage.py migrate && python direct_csv_loader.py && gunicorn --worker-tmp-dir /dev/shm turnover_prediction.wsgi:application
