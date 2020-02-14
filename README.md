# Scripts para la ejecución de experimentos en temas relacionados con el paradigma Software Defined Networks (SDN)

Los scripts fueron probados utilizando los switches HP 2920 y HP 3500yl, el controlador Aruba VAN SDN Controller y OpenFlow 1.3


### Requerimientos

Se agrega el archivo requirements.txt

## Ejemplos de ejecución

a2.py - Script para insertar flujos en la tabla con id 100 de una instancia Openflow 1.3

python3 a2.py -h
usage: a2.py [-h] -c CONTROLLER -u USER -p PASSWD -dpid DATAPATH -pid PORT -pv
             PRIORITY -s SOURCE -d DESTINATION

Ejemplo:

python3 a2.py -c 10.0.0.1 -u sdn -p skyline -dpid 00:15:64:51:06:ca:a2:c0 -pid 24 -pv 30000 -s 20.0.0.1 -d 20.0.0.2







