
"""
a7.py Obtiene los datos transmitidos en un puerto de un DPID determinado en el transcurso de un intervalo en segundos 
        e inserta el dato en una base de datos InfluxDB para graficar posteriormente utilizando Grafana

"""
import argparse
import signal
import requests
import urllib3
import json
import time
from influxdb import InfluxDBClient


def get_port_stats(ctrl, user, passwd, dpid, port, dbserver, db, dbport, dbuser, dbpass, table, field, sample):

    #Get token
    url = 'https://'+ctrl+':8443/sdn/v2.0/auth'
    data = '{"login":{"user":"'+user+'","password":"'+passwd+'","domain":"sdn"}}'
    headers_token = {"Content-Type": "application/json"}
    res_token = requests.post(url, data=data, headers=headers_token,verify=False)
    json_token = res_token.json()
    token = json_token['record']['token']

    url_stats = 'https://'+ctrl+':8443/sdn/v2.0/of/stats/ports?dpid='\
			+dpid+'&port_id='+port 

    headers_stats = {"Content-Type": "application/json", "X-Auth-Token": token}
    res_stats1 = requests.get(url_stats, headers=headers_stats, verify=False)
    json_stats1 = res_stats1.json()
    time.sleep(int(sample))
    res_stats2 = requests.get(url_stats, headers=headers_stats, verify=False)
    json_stats2 = res_stats2.json()

    if res_stats1.status_code == 201 or res_stats1.status_code == 200:
        print("Success!")
    else:
        print('An error HTTP '+str(res_stats1.status_code)+' has ocurred')

    rx_packets1 = json_stats1['port_stats']['rx_packets']
    tx_packets1 = json_stats1['port_stats']['tx_packets']
    rx_bytes1 = json_stats1['port_stats']['rx_bytes']
    tx_bytes1 = json_stats1['port_stats']['tx_bytes']
    rx_dropped1 = json_stats1['port_stats']['rx_dropped']
    tx_dropped1 = json_stats1['port_stats']['tx_dropped']
    rx_errors1 = json_stats1['port_stats']['rx_errors']
    tx_errors1 = json_stats1['port_stats']['tx_errors']
    collisions1 = json_stats1['port_stats']['collisions']

    rx_packets2 = json_stats2['port_stats']['rx_packets']
    tx_packets2 = json_stats2['port_stats']['tx_packets']
    rx_bytes2 = json_stats2['port_stats']['rx_bytes']
    tx_bytes2 = json_stats2['port_stats']['tx_bytes']
    rx_dropped2 = json_stats2['port_stats']['rx_dropped']
    tx_dropped2 = json_stats2['port_stats']['tx_dropped']
    rx_errors2 = json_stats2['port_stats']['rx_errors']
    tx_errors2 = json_stats2['port_stats']['tx_errors']
    collisions2 = json_stats2['port_stats']['collisions']


    #Port utilization formula % = (bits * 100 / bw * interval)
    port_utilization = ((((rx_bytes2+tx_bytes2)-(rx_bytes1+tx_bytes1))*8)*100)/(100000000*60)

    #InfluxDB
    dbClient = InfluxDBClient(dbserver, dbport, dbuser, dbpass, db)
    util_body = [
            {
                "measurement": "utilization",
                "tags": {
                    "host": table,
                    "port": field
                },
                "fields": {
                    "value": port_utilization
                }
            }
        ]

    dbClient.write_points(util_body)


#Entry point for program

if __name__ == '__main__':

    urllib3.disable_warnings()

    parser = argparse.ArgumentParser(description='Script que inserta una ruta de un origen a un destino')
    parser.add_argument('-c', '--controller', required=True, help='sdn controller ipv4')
    parser.add_argument('-u', '--user', required=True, help='user sdn controller')
    parser.add_argument('-p', '--passwd', required=True, help='password sdn controller')
    parser.add_argument('-dpid', '--datapath', required=True, help='Datapath ID')
    parser.add_argument('-pt', '--port', required=True, help='Port of Datapath ID')
    parser.add_argument('-ds', '--dbserver', required=True, help='db server ipv4')
    parser.add_argument('-db', '--database', required=True, help='Database')
    parser.add_argument('-dp', '--dbport', required=True, help='Database port')
    parser.add_argument('-du', '--dbuser', required=True, help='Database user')
    parser.add_argument('-dps', '--dbpass', required=True, help='Database password')
    parser.add_argument('-t', '--table', required=True, help='Database table')
    parser.add_argument('-f', '--field', required=True, help='Database field')
    parser.add_argument('-s', '--sample', required=True, help='Sample interval in seconds')
    args = parser.parse_args()

    ctrl = args.controller
    user = args.user
    passwd = args.passwd
    dpid = args.datapath
    port = args.port
    dbserver = args.dbserver
    db = args.database
    dbport = args.dbport
    dbuser = args.dbuser
    dbpass = args.dbpass
    table = args.table
    field = args.field
    sample = args.sample

    try:
        print('CTRL+C to end')
        while True:
            get_port_stats(ctrl, user, passwd, dpid, port, dbserver, db, dbport, dbuser, dbpass, table, field, sample)
    except KeyboardInterrupt:
        print('Stopped')    
    