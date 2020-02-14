"""
a4.py Obtiene los nodos vecinos de un nodo determinado

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

	
	for x in links:
		#print(x["src_dpid"],x["src_port"],x["dst_dpid"],x["dst_port"] )
		src = x["src_dpid"]
		#src_port = x["src_port"]
		dst = x["dst_dpid"]
		#dst_port = x["dst_port"]
		G.add_node(src)
		G.add_node(dst)
		G.add_edge(src,dst)

	print("====== Nodes in G ======")
	print(G.nodes(data=True))
	#Print number of nodes
	print("Number of nodes: {0}".format(G.number_of_nodes())) 
	return G

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

	Gnodes = get_links(ctrl, user, passwd)

	n = input("Enter DPID of node to get your neighbors: ")
	print("Neighbors of node {0} ".format(n))
	print(Gnodes[n])


