#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import dbus
import pickle
#import BeautifulSoup
import httplib
import ConfigParser
#import optparse
#import ansley

def loadConf(conf_file):
	"""Carga la configuración de un fichero y la guarda en un diccionario."""
	configuration = {} # Diccionario que contendrá la configuración.
	conf = ConfigParser.ConfigParser()
	try:
		 conf.readfp(file(conf_file))
	except:
		 print "Catherine: no se pudo leer el fichero de configuración '%s' ." % conf_file
		 return
	configuration['server_addr'] = conf.get('SERVER', 'Address'.lower()) # Cadena con la dirección del servidor.
	try:
		 configuration['server_port'] = conf.getint('SERVER','Port'.lower()) # Entero con el puerto por el que conectar al servidor.
	except:
		print "Catherine: valor incorrecto para el puerto del servidor, se usará el 8000."
		configuration['server_port'] = 8000
	configuration['connection'] = configuration['server_addr']+":"+str(configuration['server_port']) # Cadena de conexión, servidor:puerto.
	configuration['quiet'] = conf.getboolean('OUTPUT', 'Quiet') # Booleano para modo silencioso.
	configuration['output'] = conf.get('OUTPUT', 'Out'.lower()) # Cadena con el formato de salida (xml, db...).
	return configuration

def req_PUT(con, path, data, quiet):
	"""Realiza la petición para enviar los datos al servidor 
	mediante el método PUT del protocolo HTTP."""
	connection = httplib.HTTPConnection(con)
	if not quiet:
		print "Enviando datos al servidor (%s)..." % con
	try:
		connection.request("PUT", path, data)
	except:
		print "Hubo un error al realizar la petición."
		exit(1)
	try:
		if not quiet:
			print "Esperando respuesta..."
		respuesta = connection.getresponse()
		if not quiet:
			print respuesta.status, respuesta.reason
	except:
		print "No se pudo recibir la respuesta."
		exit(1)
	if(respuesta.status != 200):
		print "Hubo algún error en el servidor."
		exit(1)
	else:
		if not quiet:
			print "Datos enviados."

class Catherine():
	"""Clase principal del programa.
	Se comunica con HAL mediante DBUS, reúne los datos en una lista
	y os envía al servidor."""
	def __init__(self, configuration):
		self.bus = dbus.SystemBus()
		self.hal_manager_obj = self.bus.get_object("org.freedesktop.Hal", "/org/freedesktop/Hal/Manager")
		self.hal_manager = dbus.Interface(self.hal_manager_obj, "org.freedesktop.Hal.Manager")
		self.device_names = self.hal_manager.GetAllDevices() # Lista de nombres de dispositivos.
		self.computer = [] # Lista sobre la que se formará el árbol de dispositivos.

	def run(self):
		if not configuration['quiet']:
			print "Obteniendo datos..."
		self.createTree('/org/freedesktop/Hal/devices/computer', None) # /devices/computer es el primer nodo del árbol de dispositivos.
		if configuration['output'] == 'simple':
			return self.computer
#		if configuration['output'] == 'xml':
#			traductor = ansley.Ansley(self.computer)
#			print traductor.ListToXml()
#			exit()
		if configuration['output'] == 'database':
			computer_pickled = pickle.dumps(self.computer)
			req_PUT(configuration['connection'], 'path', computer_pickled, configuration['quiet'])
			exit()

	# Crea un nuevo nodo y su subnodo de propiedades.
	def newNode(self, name):
		device_dbus_obj = self.bus.get_object("org.freedesktop.Hal", name)
		properties = device_dbus_obj.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
		
		node = []
		node_properties = {}

		for property in properties:
			node_properties[str(property)] = str(properties[property])
		node.append(node_properties) # Añado el nodo propiedades al dispositivo.
		return node

	# Obtiene el padre de un dispositivo.
	def getParent(self, device):
		device_dbus_obj = self.bus.get_object("org.freedesktop.Hal", device)
		properties = device_dbus_obj.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
		for property in properties:
			if(property=='info.parent'):
				parent = str(properties[property])
		return parent

	# Obtiene una lista con los hijos de un dispositivo.
	def getChildren(self, name):
		children = []
		for device in self.device_names:
			device_dbus_obj = self.bus.get_object("org.freedesktop.Hal", device)
			properties = device_dbus_obj.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
			for property in properties:
				if((property=='info.parent') and (str(properties[property])==name)):
					children.append(str(device))
		return children

	# Crea el árbol de nodos a partir del nodo root.
	# root es el nombre del nuevo nodo, parent es el nodo del que cuelga root.
	def createTree(self, root, parent):
		node = self.newNode(root) # '/org/freedesktop/Hal/devices/computer'
		if parent == None: # Si no tiene padre, se inserta directamente en la lista. Esto sólo debería ocurrir para el primer nodo (computer).
			self.computer.append(node)
		else:
			parent.append(node)
		children = self.getChildren(root)
		for child in children:
			self.createTree(child, node)


if __name__ == "__main__":
	config_file='catherine.conf'
	configuration = loadConf(config_file)
	objeto = Catherine(configuration)
	computer_object = objeto.run()
	#print computer_object[0][0]
	exit()
