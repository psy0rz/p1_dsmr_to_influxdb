Dit script leest alle waarden van de slimme meter die ondersteund worden door de dsmr-parser module.

Dus niet alleen het verbruik maar ook interesante dingen zoals het wattage per fase of het aantal keren dat er een voltage verlaging is geweest.

Het script stuurt de informatie door naar InfluxDB. Met Grafana zijn er mooie grafieken van te maken.

Importeer de json file in garafa om meteen een mooi dashboard te krijgen.

Live demo: https://grafana1.datux.nl/d/LIOTB61Zz/power-usage?orgId=1&refresh=10s

Let op: De per-groep data komt uiteraard niet uit de P1 meter, hier heb ik losse KWH meters per groep voor gebruikt. Zie https://github.com/psy0rz/YTLmodbus
