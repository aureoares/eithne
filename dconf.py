#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import optparse

def conf_eithne():
	print "Vamos a configurar el servidor de Eithne."
	eithne_file = raw_input("Ruta para el fichero [/etc/eithne/eithne.conf]: ")
	if (eithne_file == ''):
		eithne_file = '/etc/eithne/eithne.conf'
	f = open(eithne_file, 'w')

	# Datos del servidor.
	f.write("[SERVER]\n")
	opt = raw_input("Dirección del servidor [localhost]: ")
	if (opt == 'localhost'):
		opt = ''
	line = 'Address='+opt+'\n'
	f.write(line)
	opt = raw_input("Puerto del servidor [8000]: ")
	if (opt == ''):
		opt = '8000'
	line = 'Port='+opt+'\n'
	f.write(line)

	# Datos del servidor de bases de datos.
	f.write("[DATABASE]\n")
	opt = raw_input("Dirección del servidor de la base de datos [localhost]: ")
	if (opt == ''):
		opt = 'localhost'
	line = 'Server='+opt+'\n'
	f.write(line)
	opt = raw_input("Nombre de la base de datos [eithne]: ")
	if (opt == ''):
		opt = 'eithne'
	line = 'Database='+opt+'\n'
	f.write(line)
	opt = raw_input("Nombre de usuario de la base de datos [admin]: ")
	if (opt == ''):
		opt = 'admin'
	line = 'User='+opt+'\n'
	f.write(line)
	opt = raw_input("Password del usuario [admin]: ")
	if (opt == ''):
		opt = 'admin'
	line = 'Passwd='+opt+'\n'
	f.write(line)

	f.close()

def conf_catherine():
	print "Vamos a configurar el cliente de Eithne."
	catherine_file = raw_input("Ruta para el fichero [/etc/eithne/catherine.conf]: ")
	if (catherine_file == ''):
		catherine_file = '/etc/eithne/catherine.conf'
	f = open(catherine_file, 'w')

	# Datos del servidor.
	f.write("[SERVER]\n")
	opt = raw_input("Servidor al que conectará [192.168.2.166]: ")
	if (opt == ''):
		opt = '192.168.2.166'
	line = 'Address='+opt+'\n'
	f.write(line)
	opt = raw_input("Puerto del servidor [8000]: ")
	if (opt == ''):
		opt = '8000'
	line = 'Port='+opt+'\n'
	f.write(line)

	# Datos de salida.
	f.write("[OUTPUT]\n")
	opt = raw_input("Modo silencioso (y/n) [n]: ")
	if (opt == 'y'):
		opt = 'True'
	else:
		opt = 'False'
	line = 'Quiet='+opt+'\n'
	f.write(line)
	opt = raw_input("Modo de salida (xml/database) [database]: ")
	if (opt == ''):
		opt = 'database'
	line = 'Out='+opt+'\n'
	f.write(line)

	f.close()


def conf_tftp():
	print "Vamos a configurar el servidor TFTP."
	tftp_file = raw_input("Ruta para el fichero [/etc/default/tftpd-hpa]: ")
	if (tftp_file == ''):
		tftp_file = '/etc/default/tftpd-hpa'
	f = open(tftp_file, 'w')

	f.write('RUN_DAEMON="yes"\n')
	opt = raw_input("Ruta de los ficheros de arranque [/var/lib/tftpboot]: ")
	if (opt == ''):
		opt = '/var/lib/tftpboot'
	line = 'OPTIONS="-l -s '+opt+' "\n'
	f.write(line)

	f.close()

def conf_dhcp():
	print "Vamos a configurar el servidor DHCP."
	dhcp_file = raw_input("Ruta para el fichero [/etc/dhcp3/dhcpd.conf]: ")
	if (dhcp_file == ''):
		dhcp_file = '/etc/dhcp3/dhcpd.conf'
	f = open(dhcp_file, 'w')

	f.write('authoritative;\n')
	f.write('allow booting;\n')
	f.write('allob bootp;\n')

	opt = raw_input("Dirección de red [192.168.2.0]: ")
	if (opt == ''):
		opt = '192.168.2.0'
	line = 'subnet '+opt+' '
	f.write(line)
	opt = raw_input("Máscara de red [255.255.255.0]: ")
	if (opt == ''):
		opt = '255.255.255.0'
	line = 'netmask '+opt+' {\n'
	f.write(line)

	print "Rango de direcciones que se asignarán dinámicamente:"
	opt = raw_input("Mínimo [192.168.2.1]: ")
	if (opt == ''):
		opt = '192.168.2.1'
	line = '  range '+opt+' '
	f.write(line)
	opt = raw_input("Máximo [192.168.2.254]: ")
	if (opt == ''):
		opt = '192.168.2.254'
	line = opt+';\n'
	f.write(line)

	opt = raw_input("Dirección de difusión [192.168.2.255]: ")
	if (opt == ''):
		opt = '192.168.2.255'
	line = '  option broadcast-address "'+opt+'";\n'
	f.write(line)

	opt = raw_input("Nombre de dominio [localdomain.domain]: ")
	if (opt == ''):
		opt = 'localdomain.domain'
	line = '  option domain-name "'+opt+'";\n'
	f.write(line)

	opt = raw_input("Puerta de enlace [192.168.2.166]: ")
	if (opt == ''):
		opt = '192.168.2.166'
	line = '  option routers '+opt+';\n'
	f.write(line)

	opt = raw_input("Fichero de arranque [/pxelinux.0]: ")
	if (opt == ''):
		opt = '/pxelinux.0'
	line = '  filename "'+opt+'";\n }\n'
	f.write(line)

	f.close()


def conf_nfs():
	print "Vamos a configurar el servidor NFS."
	exports_file = raw_input("Ruta para el fichero exports [/etc/exports]: ")
	if (exports_file == ''):
		exports_file = '/etc/exports'
	f = open(exports_file, 'w')

	opt = raw_input("Ruta del sistema de ficheros para el cliente [/var/lib/tftpboot/nfs]: ")
	if (opt == ''):
		opt = '/var/lib/tftpboot/nfs'
	line = opt+' 	192.168.2.*(rw,no_root_squash,async)\n'
	f.write(line)

	f.close()

def conf_adhara():
	print "Vamos a configurar Adhara."
	adhara_file = raw_input("Ruta para el fichero [/etc/eithne/adhara.conf]: ")
	if (adhara_file == ''):
		adhara_file = '/etc/eithne/adhara.conf'
	f = open(adhara_file, 'w')

	f.write('[PATHS]\n')
	opt = raw_input("Ruta para arrancar el servidor DHCP [/etc/init.d/dhcp3-server]: ")
	if (opt == ''):
		opt = '/etc/init.d/dhcp3-server'
	line = 'dhcp='+opt+'\n'
	f.write(line)
	opt = raw_input("Ruta para arrancar el servidor TFTP [/etc/init.d/tftpd-hpa]: ")
	if (opt == ''):
		opt = '/etc/init.d/tftpd-hpa'
	line = 'tftp='+opt+'\n'
	f.write(line)
	opt = raw_input("Ruta para arrancar el servidor NFS [/etc/init.d/nfs-kernel-server]: ")
	if (opt == ''):
		opt = '/etc/init.d/nfs-kernel-server'
	line = 'nfs='+opt+'\n'
	f.write(line)
	opt = raw_input("Ruta para arrancar el servidor Eithne [/usr/sbin/eithne]: ")
	if (opt == ''):
		opt = '/usr/sbin/eithne'
	line = 'eithne='+opt+'\n'
	f.write(line)

	f.close

def conf_all():
	conf_adhara()
	conf_eithne()
	conf_tftp()
	conf_dhcp()
	conf_nfs()


if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option("-a", "--all", help="crea todos los ficheros de configuracion", action="store_true", default=False)
	parser.add_option("-e", "--eithne", help="configura cliente y servidor de Eithne", action="store_true", default=False)
	parser.add_option("-d", "--dhcp", help="configura servidor dhcp", action="store_true", default=False)
	parser.add_option("-t", "--tftp", help="configura servidor tftp", action="store_true", default=False)
	parser.add_option("-r", "--rsync", help="configura demonio de rsync", action="store_true", default=False)
	options, arguments = parser.parse_args()

	if options.all:
		conf_all()
		exit()
	if options.eithne:
		conf_eithne()
	if options.tftp:
		conf_tftp()
	if options.dhcp:
		conf_dhcp()
	if options.rsync:
		conf_rsync()
	exit()
