
import os


serial_port="/dev/ttyUSB0"

#influx db http host
host=os.environ['DB_HOST']
#port="8086"
port=os.environ['DB_PORT']

username=os.environ['DB_USER']
password=os.environ['DB_PASSWORD']
database=os.environ['DB_NAME']
