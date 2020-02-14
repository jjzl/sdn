
"""
getPortStatistics.py Obtiene los datos transmitidos en un puerto de un DPID determinado en el transcurso de 60 segundos

"""
import argparse
import requests
import urllib3
import json
import time


def get_port_stats(ctrl, user, passwd):

    #Get token
    url = 'https://'+ctrl+':8443/sdn/v2.0/auth'
    data = '{"login":{"user":"'+user+'","password":"'+passwd+'","domain":"sdn"}}'
    headers_token = {"Content-Type": "application/json"}
    res_token = requests.post(url, data=data, headers=headers_token,verify=False)
    json_token = res_token.json()
    token = json_token['record']['token']

    #Get forward path
    n = input("Enter DPID of switch: ")
    dpid = n
    p = input("Enter port of switch: ")
    port_id = p
    url_stats = 'https://'+ctrl+':8443/sdn/v2.0/of/stats/ports?dpid='\
			+dpid+'&port_id='+port_id 

    headers_stats = {"Content-Type": "application/json", "X-Auth-Token": token}
    res_stats1 = requests.get(url_stats, headers=headers_stats, verify=False)
    json_stats1 = res_stats1.json()
    time.sleep(60)
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
    print('rx_packets = '+ str(rx_packets1)+','+str(rx_packets2))
    print('tx_packets = '+ str(tx_packets1)+','+str(tx_packets2))
    print('rx_bytes = '+ str(rx_bytes1)+','+str(rx_bytes2))
    print('tx_bytes = '+ str(tx_bytes1)+','+str(tx_bytes2))
    print('rx_dropped = '+ str(rx_dropped1)+','+str(rx_dropped2))
    print('tx_dropped = '+ str(tx_dropped1)+','+str(tx_dropped2))
    print('rx_errors = '+ str(rx_errors1)+','+str(rx_errors2))
    print('tx_errors = '+ str(tx_errors1)+','+str(tx_errors2))
    print('collisions = '+ str(collisions1)+','+str(collisions2))
    print('port_utilization ='+str(port_utilization))


#Entry point for program

if __name__ == '__main__':

    urllib3.disable_warnings()

    parser = argparse.ArgumentParser(description='Script que inserta una ruta de un origen a un destino')
    parser.add_argument('-c', '--controller', required=True, help='sdn controller ipv4')
    parser.add_argument('-u', '--user', required=True, help='user sdn controller')
    parser.add_argument('-p', '--passwd', required=True, help='password sdn controller')
    args = parser.parse_args()

    ctrl = args.controller
    user = args.user
    passwd = args.passwd    

    get_port_stats(ctrl, user, passwd)
