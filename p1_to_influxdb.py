#!/usr/bin/python3

from dsmr_parser import telegram_specifications, obis_references
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V4
from influxdb import InfluxDBClient
import pprint
import config
import decimal
import time


prev_gas=None
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
        print("Waiting for P1 port measurement..")


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

                if hasattr(value, "value"):
                    #determine obis name
                    for obis_name in dir(obis_references):
                        if getattr(obis_references,obis_name)==key:
                            name=obis_name
                            break
                    
                    #Filter out failure log entries
                    if name!="POWER_EVENT_FAILURE_LOG": 
                    #is it a number?
                        if isinstance(value.value, int) or isinstance(value.value, decimal.Decimal):
                            nr=float(value.value)
                            #filter duplicates gas , since its hourly. (we want to be able to differentiate it, duplicate values confuse that)
                            if name=='HOURLY_GAS_METER_READING':
                                if prev_gas!=None and nr!=prev_gas:
                                    influx_measurement['fields'][name]=float(value.value)
                                prev_gas=nr
                            else:
                                influx_measurement['fields'][name]=float(value.value)


            pprint.pprint(influx_measurement)
            if len(influx_measurement['fields']):
                db.write_points([influx_measurement])
    except Exception as e:
        print(str(e))
        print("Pausing and restarting...")
        time.sleep(10)



