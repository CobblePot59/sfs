FROM python:3.9-slim
WORKDIR /opt/sfs/sources
RUN python3 -m pip install gunicorn flask flask-sqlalchemy==2.5.1 flask-dropzone hashids asgiref bcrypt
ENV GUNICORN_CMD_ARGS="-b 0.0.0.0:80 -w 4"
EXPOSE 80
CMD ["gunicorn", "wsgi:app"]
