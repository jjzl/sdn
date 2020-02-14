

"""
a2.py Creación de rutas vía REST

"""

import urllib3
import json
import requests
import argparse


def insert_flow(ctrl, user, passwd, dpid, pid, pv, src, dst):

	#Get token
	url = 'https://'+ctrl+':8443/sdn/v2.0/auth'
	data = '{"login":{"user":"'+user+'","password":"'+passwd+'","domain":"sdn"}}'
	headers_token = {"Content-Type": "application/json"}
	res_token = requests.post(url, data=data, headers=headers_token,verify=False)
	json_token = res_token.json()
	token = json_token['record']['token']

	#Payload
	payload = '{"flow":{"cookie":"0x15081980","table_id":100,\
				"priority":'+pv+',"idle_timeout":300,"hard_timeout":300,\
				"match":[{"ipv4_src":"'+src+'"},{"ipv4_dst":"'+dst+'"},{"eth_type":"ipv4"}],\
				"instructions":[{"apply_actions":[{"output":'+pid+'}]}]}}'

	url_flow = 'https://148.247.201.101:8443/sdn/v2.0/of/datapaths/'+dpid+'/flows'

	headers_flow = {"Content-Type": "application/json", "X-Auth-Token": token}
	res_flow = requests.post(url_flow, headers=headers_flow, data=payload, verify=False)

	if res_flow.status_code == 201:
		print("Success!")
	else:
		print('An error HTTP '+str(res_flow.status_code)+' has ocurred')


#Entry point for program

if __name__ == '__main__':

	urllib3.disable_warnings()

	parser = argparse.ArgumentParser(description='Script que inserta una ruta de un origen a un destino')
	parser.add_argument('-c', '--controller', required=True, help='sdn controller ipv4')
	parser.add_argument('-u', '--user', required=True, help='user sdn controller')
	parser.add_argument('-p', '--passwd', required=True, help='password sdn controller')
	parser.add_argument('-dpid', '--datapath', required=True, help='DatapathID')
	parser.add_argument('-pid', '--port', required=True, help='Port DatapathID')
	parser.add_argument('-pv', '--priority', required=True, help='Priority value')
	parser.add_argument('-s', '--source', required=True, help='ipv4_src')
	parser.add_argument('-d', '--destination', required=True, help='ipv4_dst')
	args = parser.parse_args()

	ctrl = args.controller
	user = args.user
	passwd = args.passwd
	dpid = args.datapath
	pid = args.port
	pv = args.priority
	src = args.source
	dst = args.destination

	insert_flow(ctrl, user, passwd, dpid, pid, pv, src, dst)
