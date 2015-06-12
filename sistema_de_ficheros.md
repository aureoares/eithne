# Introducción #

> Para el arranque en red necesitamos crear el sistema de ficheros que utilizarán los clientes.

# Pasos a seguir #

  * Usaremos debootstrap para crear el sistema de ficheros y a continuación le haremos las modificaciones que necesitamos:
```
 sudo debootstrap --include=dbus,hal,python2.5,python-dbus,initramfs-tools,linux-image intrepid /var/lib/tftpboot/nfs
```
    * Incluímos los paquetes dbus, hal, python2.5 y python-dbus porque los necesitaremos para hacer funcionar nuestra aplicación cliente. Initramfs-tools y linux-image los necesitaremos a continuación.
    * Para más información, consultar la documentación de debootstrap y initramfs-tools.

  * Vamos a crear los ficheros de arranque que necesitamos:
```
 sudo nano /var/lib/tftpboot/nfs/etc/initramfs-tools/initramfs.conf
```
    * Las líneas importantes son:
```
 MODULES=netboot
 BOOT=nfs
 DEVICE=eth0 	# O la interfaz que se utilice para el arranque.
 NFSROOT=auto
```
    * Hacemos chroot al nuevo sistema y creamos el initrd.img :
```
 sudo chroot /var/lib/tftpboot/nfs
 mkinitramfs -o /boot/initrd.img-<versión>
```
    * ¡Importante haber hecho chroot primero!
    * Salimos del sistema:
```
 exit
```
    * Copiamos los ficheros de arranque y creamos la configuración:
```
 sudo cp /var/lib/tftpboot/nfs/boot/initrd.img-<versión> /var/lib/tftpboot/initrd.img
 sudo cp /var/lib/tftpboot/nfs/boot/vmlinuz-<versión> /var/lib/tftpboot/kernel
 sudo cp /usr/lib/syslinux/pxelinux.0 /var/lib/tftpboot/pxelinux.0
 sudo mkdir /usr/lib/tftpboot/pxelinux.cfg
 sudo nano /usr/lib/tftpboot/pxelinux.cfg/default

 LABEL linux
 KERNEL kernel
 APPEND vga=extended initrd=initrd.img root=/dev/nfs nfsroot=192.168.2.166:/var/lib/tftpboot/nfs ip=dhcp rw
```
    * Estos 4 ficheros deben tener permisos de lectura (chmod 644).

  * Otros ajustes:
```
 sudo nano /var/lib/tftpboot/nfs/etc/network/interfaces

 auto lo
 iface lo inet loopback
 	iface eth0 inet manual

 sudo nano /var/lib/tftpboot/nfs/etc/fstab

 proc      /proc      proc   defaults  0  0
 /dev/nfs  /          nfs  	defaults  1  1
 none      /tmp       tmpfs  defaults  0  0
 none      /var/run   tmpfs  defaults  0  0
 none      /var/lock  tmpfs  defaults  0  0
 none      /var/tmp   tmpfs  defaults  0  0
```

  * En este punto el sistema estaría listo para arrancar en red, montar el sistema de ficheros y mostrar el login. Sólo nos falta añadirle el cliente y hacer que se ejecute al finalizar el arranque del sistema:
```
 sudo cp catherine.py /var/lib/tftpboot/nfs/root/catherine.py
 sudo cp catherine.conf /var/lib/tftpboot/nfs/etc/eithne/catherine.conf
 sudo nano /var/lib/tftpboot/nfs/etc/rc.local

 #!/bin/sh -e
 echo
 echo
 echo “Finalizado el arranque, va a ejecutarse Catherine.”
 echo “Si todo va bien, el equipo se apagará automáticamente cuando haya terminado.”
 echo
 echo /root/catherine.py && poweroff
```

# Lo que quedaría por hacer #

> Habría que hacer limpieza en el sistema de todo lo que no sea estrictamente necesario para nuestro propósito, tanto de los scripts de arranque como de todo el sistema de ficheros.