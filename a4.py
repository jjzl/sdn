"""
a4.py Obtiene los enlaces disponibles entre los nodos de una topologia

"""
import argparse
import requests
import urllib3
import json
import networkx as nx
import matplotlib.pyplot as plt


def get_links(ctrl, user, passwd):

	G = nx.Graph()

	#Get token
	url = 'https://'+ctrl+':8443/sdn/v2.0/auth'
	data = '{"login":{"user":"'+user+'","password":"'+passwd+'","domain":"sdn"}}'
	headers_token = {"Content-Type": "application/json"}
	res_token = requests.post(url, data=data, headers=headers_token,verify=False)
	json_token = res_token.json()
	token = json_token['record']['token']

	#Get links info
	url_links = 'https://'+ctrl+':8443/sdn/v2.0/net/links'
	headers_links = {"Content-Type": "application/json", "X-Auth-Token": token}
	res_links = requests.get(url_links, headers=headers_links, verify=False)
	links = res_links.json()["links"]

	print("======src_dpid===src_port===dst_dpid===dst_port======")
	for x in links:
		print(x["src_dpid"],x["src_port"],x["dst_dpid"],x["dst_port"] )
		src = x["src_dpid"]
		src_port = x["src_port"]
		dst = x["dst_dpid"]
		dst_port = x["dst_port"]
		G.add_node(src)
		G.add_node(dst)
		G.add_edge(src,dst)

	#Print edges
	print("====================================Edges=======================================")
	print(G.edges.data())
	#Print number of edges
	print("##### Number of edges: {0}".format(G.number_of_edges())) 
	#print(G.number_of_edges())

	#Print Neighbors Example
	#n = 'datapathID'
	#print(G[n])

	#Print topology
	#plt.subplot(121)
	#plt.figure(figsize=(20, 20), dpi=80)
	#nx.draw(G, with_labels=True, font_weight='bold')
	#plt.show()

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

	get_links(ctrl, user, passwd)
