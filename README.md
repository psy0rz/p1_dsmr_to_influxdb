Dit script leest alle waarden van de slimme meter die ondersteund worden door de dsmr-parser module.

Dus niet alleen het verbruik maar ook interesante dingen zoals het wattage per fase of het aantal keren dat er een voltage verlaging is geweest.

Het script stuurt de informatie door naar InfluxDB. Met Grafana zijn er mooie grafieken van te maken.

Importeer de json file in garafa om meteen een mooi dashboard te krijgen.

Live demo: https://grafana1.datux.nl/d/LIOTB61Zz/power-usage?orgId=1&refresh=10s


Additional Python3 libraries:

- sudo apt install python3-pip
- sudo pip3 install dsmr_parser influxdb
