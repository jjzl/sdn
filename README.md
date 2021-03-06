# Scripts para la ejecución de experimentos en temas relacionados con el paradigma Software Defined Networks (SDN)

Los scripts fueron probados utilizando los switches HP 2920 y HP 3500yl, el controlador Aruba VAN SDN Controller y OpenFlow 1.3


## Requerimientos

Se agrega el archivo requirements.txt

## Ejecución

### a2.py - Script para insertar flujos en la tabla con id 100 de una instancia Openflow 1.3

python3 a2.py -h
usage: a2.py [-h] -c CONTROLLER -u USER -p PASSWD -dpid DATAPATH -pid PORT -pv
             PRIORITY -s SOURCE -d DESTINATION

Ejemplo:

python3 a2.py -c 10.10.10.101 -u sdn -p skyline -dpid 00:15:64:51:06:ca:a2:c0 -pid 24 -pv 30000 -s 20.0.0.1 -d 20.0.0.2


### a3.py - Script para insertar configuracion en un equipo de red

python3 a3.py -h
usage: a3.py [-h] -i IP -u USER -p PASSWD -c CFG -t TYPE

Ejemplo:

python3 a3.py -i 10.10.10.103 -u manager -p adminpass -c config_changes.txt -t hp_procurve


### a4.py - Script para obtener los enlaces disponibles entre los nodos de una topologia a partir del controlador SDN

python3 a4.py -h
usage: a4.py [-h] -c CONTROLLER -u USER -p PASSWD

Ejemplo:

python3 a4.py -c 10.10.10.101 -u sdn -p skyline

### a5.py - Script para obtener los nodos vecinos de un nodo determinado a partir del controlador SDN

python3 a5.py -h
usage: a5.py [-h] -c CONTROLLER -u USER -p PASSWD

Ejemplo:

python3 a5.py -c 10.10.10.101 -u sdn -p skyline

### a6.py - Script para obtener los datos transmitidos en un puerto de un DPID determinado en el transcurso de 60 segundos

python3 a6.py -h
usage: a6.py [-h] -c CONTROLLER -u USER -p PASSWD

Ejemplo:

python3 a6.py -c 10.10.10.101 -u sdn -p skyline

### a7.py - Script para obtener los datos transmitidos en un puerto de un DPID determinado cada 60 segundos e insertarlos en una base de datos en InfluxDB y desplegarlos en un dashboard de Grafana


python3 a7.py -h
usage: a7.py [-h] -c CONTROLLER -u USER -p PASSWD -dpid DATAPATH -pt PORT -ds
             DBSERVER -db DATABASE -dp DBPORT -du DBUSER -dps DBPASS -t TABLE
             -f FIELD -s SAMPLE

Ejemplo:

python3 a7.py -c 10.10.10.101 -u sdn -p skyline -dpid 00:0b:64:51:06:ca:a2:c0 -pt 4 -ds localhost -dp 8086 -du root -dps root -db bw -t sw3 -f 4 -s 60

Requerimientos:

InfluxDB, Grafana v6.4.3 