#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import BeautifulSoup
import MySQLdb

class Ansley():
	"""Clase traductora.
	
	Traduce un objeto (lista) con la información de un equipo a distintos
	formatos y viceversa.
	
	Implementados:
		- Lista a XML.
		- Lista a Base de Datos.
		- Base de Datos a Lista.
	"""

	def __init__(self, computer_object):
		self.computer = computer_object

	def getNodeName(self, node_object):
		for child in node_object:
			if type(child) is dict:
				properties = child
		if properties['info.udi']=='/org/freedesktop/Hal/devices/computer':
			return 'Computer'
		if properties.has_key('info.subsystem'):
			return properties['info.subsystem']
		if properties.has_key('info.category'):
			return properties['info.category']
		if properties.has_key('info.product'):
			return properties['info.product']
		return properties['info.udi']

	def ListToXml(self):
		self.document = BeautifulSoup.BeautifulSoup() # Documento que contendrá el XML.
		self.createTreeXml(0, self.computer[0], None)
		return self.document
	
	def ListToDb(self, user, passwd, database, server, network_id):
		self.database = database
		self.server = server
		self.user = user
		self.passwd = passwd
		self.network_id = network_id
		# Conectamos con la base de datos.
		try:
			self.connection = MySQLdb.connect(user=self.user, passwd=self.passwd, db=self.database, host=self.server)
		except:
			print "Ansley: No se pudo conectar con la base de datos: %s." % self.database
			exit()
		self.cursor = self.connection.cursor()
		# Añado el equipo a la red.
		self.cursor.execute('''insert into COMPUTERS (Name) values ("Sin nombre")''')
		self.computer_id = self.cursor.lastrowid
		self.cursor.execute('''insert into MEMBERS (Network, Computer) values (%s,%s)''', (self.network_id, self.computer_id))
		self.connection.commit()
		self.createTreeDb(self.computer[0], None)

	def DbToList(self, user, passwd, database, server, computer_id):
		self.database = database
		self.server = server
		self.user = user
		self.passwd = passwd
		self.computer_id = computer_id
		# Conectamos con la base de datos.
		try:
			self.connection = MySQLdb.connect(user=self.user, passwd=self.passwd, db=self.database, host=self.server)
		except:
			print "Ansley: No se pudo conectar con la base de datos: %s." % self.database
			exit()
		self.cursor = self.connection.cursor()
		self.cursor.execute('''select IDTyp from PRO_TYPES where Type like "info.udi"''')
		row = self.cursor.fetchone()
		ProKey = row[0]
		self.cursor.execute('''select IDDev from DEVICES inner join PROPERTIES on IDDev=Device where ProKey=%s and Computer=%s and ProValue like "/org/freedesktop/Hal/devices/computer"''', (ProKey, self.computer_id))
		row = self.cursor.fetchone()
		root_id = row[0]
		self.recreateTreeDb(root_id, None)

	def newNodeXml(self, node_object):
		for child in node_object:
			if type(child) is dict:
				properties = child

		node = BeautifulSoup.Tag(self.document, 'node') # Nodo del dispositivo.
		node['type'] = self.getNodeName(node_object)
		node_properties = BeautifulSoup.Tag(self.document, 'properties') # Nodo con las propiedades del dispositivo.
		#node_properties['name'] = 'properties'

		i = 0
		for property in properties.items():
			subnode_property = BeautifulSoup.Tag(self.document, 'property') # Nodo que contiene la propiedad.
			subnode_property['type'] = property[0]
			text = BeautifulSoup.NavigableString(str(property[1])) # Valor de la propiedad.
			subnode_property.insert(0, text)
			node_properties.insert(i, subnode_property) # Añado la propiedad al nodo propiedades.
			i = i+1
		node.insert(0,node_properties) # Añado el nodo propiedades al dispositivo.
		return node

	def newNodeDb(self, node_object, parent_id):
		# Añadimos el dispositivo al equipo.
		if(parent_id == None):
			self.cursor.execute('''insert into DEVICES (Parent, Computer) values (NULL,%s)''', (self.computer_id,))
		else:
			self.cursor.execute('''insert into DEVICES (Parent, Computer) values (%s,%s)''', (parent_id, self.computer_id))
		device_id = self.cursor.lastrowid
		self.connection.commit()
		# Obtenemos el diccionario de propiedades.
		for child in node_object:
			if type(child) is dict:
				properties = child
		# Añadimos las propiedades al dispositivo.
		for property in properties.items():
			# Comprobamos si el tipo de propiedad existe o hay que crearlo.
			self.cursor.execute('''select IDTyp from PRO_TYPES where Type like %s''', (property[0],))
			if(self.cursor.rowcount > 0):
				row = self.cursor.fetchone()
				type_id = row[0]
			else:
				self.cursor.execute('''insert into PRO_TYPES (Type) values (%s)''', (property[0],))
				type_id = self.cursor.lastrowid
				self.connection.commit()
			# Añado la propiedad al dispositivo.
			self.cursor.execute('''insert into PROPERTIES (ProKey, ProValue, Device) values (%s,%s,%s)''', (type_id, property[1], device_id))
			self.connection.commit()
		return device_id

	def createTreeXml(self, position, root, parent):
		node = self.newNodeXml(root) # self.computer
		if parent == None: # Si no tiene padre, se inserta directamente en el documento. Esto sólo debería ocurrir para el primer nodo (computer).
			self.document.insert(0, node)
		else:
			parent.insert(position, node)
		position = position + 1
		for child in root:
			if type(child) is list:
				self.createTreeXml(position, child, node)

	def createTreeDb(self, root, parent_id):
		device_id = self.newNodeDb(root, parent_id)

		for child in root:
			if type(child) is list:
				self.createTreeDb(child, device_id)

	def recreateTreeDb(self, root_id, parent):
		node = self.recreateNewNodeDb(root_id) # ID de Computer
		if parent == None: # Si no tiene padre, se inserta directamente en la lista. Esto sólo debería ocurrir para el primer nodo (computer).
			self.computer.append(node)
		else:
			parent.append(node)
		children = self.getChildrenDb(root_id)
		for child in children:
			self.recreateTreeDb(child[0], node)

	def recreateNewNodeDb(self, device_id):
		self.cursor.execute('''select ProKey, ProValue from PROPERTIES where Device=%s''', (device_id,))
		properties = self.cursor.fetchall()
		self.cursor.execute('''select IDTyp, Type from PRO_TYPES''')
		types = self.cursor.fetchall()
		types_dict = dict(types)
		
		node = []
		node_properties = {}

		for property in properties:
			type = property[0]
			key = types_dict[type]
			value = str(property[1])
			node_properties[key] = value
		node.append(node_properties) # Añado el nodo propiedades al dispositivo.
		return node

	def getChildrenDb(self, device_id):
		self.cursor.execute('''select IDDev from DEVICES where Parent=%s''', (device_id,))
		children = self.cursor.fetchall()
		return children
