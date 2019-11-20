#!/usr/bin/python3

from dsmr_parser import telegram_specifications, obis_references
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V4
from influxdb import InfluxDBClient
import pprint
import config
import decimal
import time

while True:
    try:
        #influx db settings
        db = InfluxDBClient(config.host,config.port, config.username, config.password, config.database)

        #serial port settings and version
        serial_reader = SerialReader(
            device=config.serial_port,
            serial_settings=SERIAL_SETTINGS_V4,
            telegram_specification=telegram_specifications.V4
        )

        print("Connecting db")
        db.create_database('energy')
        

        #read telegrams
        print("Waiting for next P1 port measurement..")
        for telegram in serial_reader.read():
            influx_measurement={
                "measurement": "P1 values",
                # "tags": {
                #     "host": "server01",
                #     "region": "us-west"
                # },
                "fields": {
                }
            }
            report=[]

            #create influx measurement record
            for key,value in telegram.items():
                name=key
                
                for obis_name in dir(obis_references):
                    if getattr(obis_references,obis_name)==key:
                        name=obis_name
                        break
                
                #add to influxdb points list?
                if isinstance(value.value, int) or isinstance(value.value, decimal.Decimal):
                    influx_measurement['fields'][name]=float(value.value)

                report.append("{} = {} {}".format(name, value.value, value.unit or ""))

            report.sort()
            pprint.pprint(report)
            print()

            print(influx_measurement)
            db.write_points([influx_measurement])
    except Exception as e:
        print(str(e))
        print("Pausing and restarting...")
        time.sleep(10)



