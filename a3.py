
"""
a3.py Insertar rate-limit en la configuración de los switches HP 2920 y HP 3500

"""
import argparse
from netmiko import ConnectHandler
from netmiko.ssh_exception import AuthenticationException, NetMikoTimeoutException

def insert_config(ip, user, passwd, cfg, dtype):

	nxos1 = {
    	"host": ip,
    	"username": user,
  		"password": passwd,
    	"device_type": dtype,
	}
	print("##### Connecting to Device {0} #####".format(nxos1['host'])) 

	try:
		
		cfg_file = cfg
		net_connect = ConnectHandler(**nxos1)
		output = net_connect.send_config_from_file(cfg_file)
		#print(output)
		net_connect.save_config()
		net_connect.disconnect()
		print("Success!")
	
	except NetMikoTimeoutException:
		print("====== SOMETHING WRONG HAPPEN WITH {0} ======".format(nxos1['host']))
	except AuthenticationException:
		print("====== AUTHENTICATION FILED WITH {0} ======".format(nxos1['host']))
	except Exception as unknown_error:
		print("====== SOMETHING UNKNOWN HAPPEN WITH {0} ======".format(nxos1['host']))

#Entry point for program

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Script que inserta parametros de configuracion en un dispositivo de red')
	parser.add_argument('-i', '--ip', required=True, help='Direccion IP del equipo')
	parser.add_argument('-u', '--user', required=True, help='Usuario administrador del equipo')
	parser.add_argument('-p', '--passwd', required=True, help='Password de administrador')
	parser.add_argument('-c', '--cfg', required=True, help='Archivo con los parametros de configuracion')
	parser.add_argument('-t', '--type', required=True, help='Tipo de dispositivo')
	args = parser.parse_args()

	ip = args.ip
	user = args.user
	passwd = args.passwd
	cfg = args.cfg
	dtype = args.type
	

	insert_config(ip, user, passwd, cfg, dtype)