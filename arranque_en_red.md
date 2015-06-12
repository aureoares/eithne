

# Introducción #

> Este es uno de los aspectos más importantes del sistema. Aunque la aplicación cliente (catherine.py) puede ejecutarse manualmente, el arranque en red hace que este proyecto sea mucho más flexible y termina de darle ese carácter automático que se pretende conseguir.

> Esta parte está basada en el [HowTo de arranque sin disco de Ubuntu](https://help.ubuntu.com/community/DisklessUbuntuHowto) con las modificaciones oportunas.

# Requisitos #

  * Un equipo para utilizar de servidor. Por comodidad usaremos un equipo servidor con todos los servicios necesarios, pero no es obligatorio que se estén todos ubicados en el mismo equipo.
  * Sistema operativo Ubuntu 8.10 o posterior. Al igual que con el resto del proyecto es probable que nos sirva cualquier otra distribución basada en Debian, pero no se ha probado.
  * Servidor DHCP. Usaremos dhcp3-server.
  * Servidor TFTP. Usaremos tftp-hpa.
  * Servidor NFS. Usaremos nfs-kernel-server.
  * Suficiente espacio en disco para el sistema de ficheros que vayamos a generar. Generalmente entre 100 y 500 MB.

# Preparando los servicios #

  * Primero instalamos los paquetes necesarios:
    * sudo apt-get install dhcp3-server tftpd-hpa nfs-kernel-server debootstrap syslinux
  * Configuramos el servidor TFTP:
    * sudo nano /etc/default/tftp-hpa
    * Debería quedar algo parecido a esto:
```
   RUN_DAEMON="yes"
   OPTIONS="-l -s /var/lib/tftpboot"
```
    * /var/lib/tftpboot será el directorio raíz para el servidor TFTP.
  * Configuramos el servidor DHCP:
    * sudo nano /etc/dhcp3/dhcpd.conf
    * Debería quedar algo parecido a esto:
```
   authoritative;
   allow booting;
   allow bootp;

   subnet 192.168.2.0 netmask 255.255.255.o {
     range 192.168.2.2 192.168.2.253;
     option broadcast-address 192.168.2.255;
     option domain-name-servers 192.168.2.166;
     option domain-name “localdomain.domain”;
     option routers 192.168.2.166;
     filename "pxelinux.0";
    }
```
    * filename es el fichero de arranque. La ruta es relativa a partir de la raíz del servidor TFTP.
  * Configuramos el servidor NFS:
    * Creamos el directorio que vamos a compartir:
```
   sudo mkdir /var/lib/tftpboot/nfs
```
    * Añadimos la siguiente línea al fichero /etc/exports :
```
   /var/lib/tftpboot/nfs    192.168.2.*(rw,no_root_squash,async)
```
    * Lo actualizamos:
```
   sudo exportfs -rv
```

# Preparando el sistema de ficheros #

> En la página [sistema\_de\_ficheros](sistema_de_ficheros.md) se describe el proceso para crearlo y dejarlo listo.

# Terminando #

> Sólo queda iniciar los servicios:
```
 sudo /etc/init.d/dhcp3-server start
 sudo /etc/init.d/tftpd-hpa start
 sudo /etc/init.d/nfs-kernel-server start
 sudo eithne.py
```
> Y ya podemos encender el equipo cliente para comprobar que todo ha salido bien. Por supuesto, primero hay que comprobar que el equipo cliente está configurado para arrancar mediante PXE.