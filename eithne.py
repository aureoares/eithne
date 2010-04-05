#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import ConfigParser
#import optparse
import pickle
#import BeautifulSoup
import MySQLdb
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import ansley

def loadConf(conf_file):
	"""Carga la configuración de un fichero y la guarda en un diccionario."""

	configuration = {} # Diccionario que contendrá la configuración.
	conf = ConfigParser.ConfigParser()
	try:
		 conf.readfp(file(conf_file))
	except:
		 print "Eithne: no se pudo leer el fichero de configuración '%s' ." % conf_file
		 return
	configuration['server_addr'] = conf.get('SERVER', 'Address'.lower())
	try:
		 configuration['server_port'] = conf.getint('SERVER','Port'.lower())
	except:
		print "Catherine: valor incorrecto para el puerto del servidor, se usará el 8000."
		configuration['server_port'] = 8000
	# Configuración para la conexión con la base de datos.
	configuration['dbserver'] = conf.get('DATABASE', 'Server'.lower())
	configuration['db'] = conf.get('DATABASE', 'Database'.lower())
	configuration['dbuser'] = conf.get('DATABASE', 'User')
	configuration['dbpasswd'] = conf.get('DATABASE', 'Passwd')
	return configuration

class MiManejador(BaseHTTPServer.BaseHTTPRequestHandler):
	"""Handler para el servidor HTTP.
	Implementa los métodos PUT y GET adaptados a la aplicación."""

	def do_PUT(self):
		"""El método PUT recoge una cadena empaquetada mediante pickle,
		recupera el objeto con la información del equipo y la almacena
		en la base de datos."""

		print 'Conectado PUT '+str(self.client_address)
		self.send_response(200, 'OK')
		self.end_headers()
		self.request.close()
		database = str(self.client_address[0])
		print 'Recogiendo datos...'
		computer_pickled = str(self.rfile.read())
		computer_object = pickle.loads(computer_pickled)
		traductor = ansley.Ansley(computer_object)
		print 'Introduciendo datos en la Base de Datos...'
		traductor.ListToDb(configuration['dbuser'], configuration['dbpasswd'], configuration['db'], configuration['dbserver'], configuration['network_id'])
		#traductor.printNodes()
		#traductor.printNodeProperties(1)
		print 'Petición finalizada.'

	def do_GET(self):
		"""El método GET recibe un path de la forma /red/equipo y 
		devuelve el informe XML correspondiente."""

		print 'Conectado GET '+str(self.client_address)
		self.send_response(200, 'OK')
		self.end_headers()
		try:
			network_id = self.path.split('/')[1]
			computer_id = self.path.split('/')[2]
		except:
			self.wfile.write('Ruta incorrecta.')
			self.request.close()
			return
		# Conectamos con la base de datos.
		try:
			connection = MySQLdb.connect(user=configuration['dbuser'], passwd=configuration['dbpasswd'], db=configuration['db'], host=configuration['dbserver'])
		except:
			print "Eithne: No se pudo conectar con la base de datos: %s." % self.database
			return
		cursor = connection.cursor()
		cursor.execute('''select IDMem from MEMBERS where Computer=%s and Network=%s''', (computer_id, network_id))
		if(cursor.rowcount == 0):
			self.wfile.write('El equipo no existe o no pertenece a la red.')
			self.request.close()
			return
		computer = []
		traductor = ansley.Ansley(computer)
		traductor.DbToList(configuration['dbuser'], configuration['dbpasswd'], configuration['db'], configuration['dbserver'], computer_id)
		document = traductor.ListToXml()
		pretty_document = document.prettify()
		pretty_document = '<?xml version="1.0" standalone="yes" ?>'+pretty_document
		self.wfile.write(pretty_document)
		self.request.close()

class ThreadingHTTPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer, BaseHTTPServer.HTTPServer):
	pass

if __name__ == "__main__":
	config_file='/etc/eithne/eithne.conf'
	configuration = loadConf(config_file)

	# Conectamos con la base de datos.
	try:
		connection = MySQLdb.connect(user=configuration['dbuser'], passwd=configuration['dbpasswd'], db=configuration['db'], host=configuration['dbserver'])
	except:
		print "Eithne: No se pudo conectar con la base de datos: %s." % configuration['db']
		exit()
	cursor = connection.cursor()

	cursor.execute('''set character_set_client = utf8''')
	cursor.execute('''set character_set_results = utf8''')

	# Pedimos los datos de la red.
	network_name = raw_input("Introduzca un nombre para identificar la red: ")

	# Comprobamos si la red existe en la base de datos.
	# Si ya existe, preguntamos si sustituirla o escoger otro nombre.
	net_ok = 'n'
	while(net_ok != 'y'):
		cursor.execute('''select IDNet from NETWORKS where Name like %s''', (network_name,))
		if(cursor.rowcount > 0):
			row = cursor.fetchone()
			net_id = row[0]
			print "La red %s ya existe en la base de datos." % network_name
			net_ok = raw_input("¿Sustituir? (y/n/a): ") # yes / no / add
			if(net_ok == 'y'):
				print "Eliminando la red anterior..."
				# Busco los equipos de la red.
				cursor.execute('''select Computer from MEMBERS where Network=%s''', (net_id,))
				computers = cursor.fetchall()
				# Por cada equipo busco los dispositivos que tiene.
				for computer in computers:
					cursor.execute('''select IDDev from DEVICES where Computer=%s''', (computer[0],))
					devices = cursor.fetchall()
					# Por cada dispositivo elimino sus propiedades.
					for device in devices:
						cursor.execute('''delete from PROPERTIES where Device=%s''', (device[0],))
					# Elimino el dispositivo
					cursor.execute('''delete from DEVICES where Computer=%s''', (computer[0],))
					# Elimino la relación entre el equipo y la red.
					cursor.execute('''delete from MEMBERS where Computer=%s and Network=%s''', (computer[0],net_id))
					# Elimino el equipo.
					cursor.execute('''delete from COMPUTERS where IDCom=%s''', (computer[0],))
				# Elimino la red.
				cursor.execute('''delete from NETWORKS where IDNet=%s''', (net_id,))
				connection.commit()
			else:
				if(net_ok == 'a'):
					net_ok = 'y'
				else:
					network_name = raw_input("Introduzca un nombre para identificar la red: ")
		else:
			net_ok = 'y'

	network_desc = raw_input("Descripción de la red: ")
	network_addr = raw_input("Dirección IP de la red: ")
	network_mask = raw_input("Máscara de red: ")

	print "Creando la nueva red..."
	cursor.execute('''insert into NETWORKS (Name, Description, IP, Netmask, Parent) values (%s,%s,%s,%s,NULL)''', (network_name, network_desc, network_addr, network_mask))
	configuration['network_id'] = cursor.lastrowid
	connection.commit()

	Clase_Servidor = ThreadingHTTPServer
	Clase_Manejador = MiManejador
	Dir_Servidor = (configuration['server_addr'], configuration['server_port'])
	httpd = Clase_Servidor(Dir_Servidor, Clase_Manejador)
	print "Iniciando servidor HTTP (%s:%s) ID: %s." % (configuration['server_addr'], configuration['server_port'], configuration['network_id'])
	httpd.serve_forever()
