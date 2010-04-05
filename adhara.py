#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import ConfigParser
import optparse
import dconf

def loadConf(conf_file):
	"""Carga la configuración de un fichero y la guarda en un diccionario."""

	configuration = {} # Diccionario que contendrá la configuración.
	conf = ConfigParser.ConfigParser()
	try:
		 conf.readfp(file(conf_file))
	except:
		 print "Adhara: no se pudo leer el fichero de configuración '%s' ." % conf_file
		 return
	configuration['dhcp_path'] = conf.get('PATHS', 'dhcp')
	configuration['tftp_path'] = conf.get('PATHS', 'tftp')
	configuration['nfs_path'] = conf.get('PATHS', 'nfs')
	configuration['eithne_path'] = conf.get('PATHS', 'eithne')
	return configuration


if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option("-c", "--config", action="store", default="")
	parser.add_option("-s", "--start", action="store", default="")
	options, arguments = parser.parse_args()
	configuration = loadConf('/etc/eithne/adhara.conf')

	if options.config:
		services = options.config.split(',')
		if 'all' in services:
			dconf.conf_all()
		else:
			if 'dhcp' in services:
				dconf.conf_dhcp()
			if 'tftp' in services:
				dconf.conf_tftp()
			if 'nfs' in services:
				dconf.conf_nfs()
			if 'eithne' in services:
				dconf.conf_eithne()
			if 'catherine' in services:
				dconf.conf_catherine()
			if 'adhara' in services:
				dconf.conf_adhara()
			
	if options.start:
		services = options.start.split(',')
		if 'all' in services:
				line = configuration['dhcp_path']+' start'
				os.system(line)
				line = configuration['tftp_path']+' start'
				os.system(line)
				line = configuration['nfs_path']+' start'
				os.system(line)
				line = 'sudo '+configuration['eithne_path']
				os.system(line)
		else:
			if 'dhcp' in services:
				line = configuration['dhcp_path']+' start'
				os.system(line)
			if 'tftp' in services:
				line = configuration['tftp_path']+' start'
				os.system(line)
			if 'nfs' in services:
				line = configuration['nfs_path']+' start'
				os.system(line)
			if 'eithne' in services:
				line = configuration['eithne_path']
				os.system(line)

	exit()
