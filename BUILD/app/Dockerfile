FROM python:slim-buster

WORKDIR /opt/sfs/sources

RUN python3 -m pip install --no-cache-dir gunicorn flask flask-sqlalchemy flask-dropzone hashids aioflask bcrypt asgiref

EXPOSE 80

CMD ["gunicorn", "wsgi:app", "--bind=0.0.0.0:80", "--workers=4", "--reload"]
