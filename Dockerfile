FROM python:3.11-alpine

WORKDIR /app
COPY  requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY config.py p1_to_influxdb.py /app/
CMD python -u p1_to_influxdb.py




