FROM python:3.8-slim

# RUN mkdir /app
RUN pwd
WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

# COPY app.py /server/app
# COPY gunicorn_config.py /server/app
# COPY wsgi.py /server/app
ADD . /app
RUN ls -l

#CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "main:app"]
# EXPOSE 5000
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "app.wsgi:app"]
# ENTRYPOINT ["gunicorn", "-w", "4", "--threads", "4", "-t", "120", "-b", "0.0.0.0:5000", "app.wsgi:app"]
# ENTRYPOINT ["python", "/app/app.py"]
# CMD ["python", "/app/app.py"]