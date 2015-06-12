
> # Módulos #

> ## Estándar de Python ##

  * dbus: para la comunicación con HAL.
  * pickle: para empaquetar y desempaquetar los datos al enviarlos al servidor.
  * httplib: para realizar las peticiones HTTP al servidor.
  * ConfigParser: para leer los ficheros de configuración.
  * optparse: para manejar los parámetros recibidos.
  * SocketServer y BaseHTTPServer: para crear el servidor HTTP.

> ## No estándar de Python ##

  * BeautifulSoup: para manejar documentos XML.
  * MySQLdb: para la comunicación con la base de datos MySQL.

> ## Módulos propios ##

  * eithne.py
    * Depende de: ansley.py
    * Utilizado por: nadie
    * Se trata de un servidor HTTP que maneja peticiones mediante el método PUT para recoger una estructura de datos con la información de un equipo e introducirla en la base de datos, y mediante el método GET para proporcionar informes consultando la información almacenada en la base de datos.

  * catherine.py
    * Depende de: ansley.py
    * Utilizado por: nadie
    * Aplicación cliente que reúne la información de hardware de un equipo haciendo consultas a HAL mediante DBUS, la organiza y realiza un informe o la envía al servidor.

  * ansley.py
    * Depende de: nadie.
    * Utilizado por: eithne.py, catherine.py
    * Realiza traducciones utilizando la estructura de datos creada por catherine.py. Convierte dicha estructura a distintos formatos y viceversa.

  * adhara.py
    * Depende de: dconf.py
    * Utilizado por: nadie
    * Herramienta de control y configuración de los distintos servidores.

  * dconf.py
    * Depende de: nadie
    * Utilizado por: adhara.py
    * Crea los ficheros de configuración para los distintos servidores a partir de ciertos datos proporcionados por el usuario.

> ## Interfaz web ##
> La interfaz web está desarrollada en HTML, PHP y Javascript. Está distribuida de la siguiente manera:

  * index.php
    * Página principal de la aplicación.
  * scripts/
    * Bibliotecas de funciones propias.
    * client.js
      * Funciones de validación en cliente.
    * server.php
      * Funciones de validación en servidor.
    * functions.php
      * Otras funciones, principalmente para generar el contenido de la página.
    * mysql.php
      * Funciones para comunicarse con la base de datos.
    * login.php
      * Procesamiento del inicio de sesión.
    * logout.php
      * Procesamiento del cierre de sesión.
    * send\_request.php
      * Procesamiento del formulario para generar informes. Valida los datos y genera la petición adecuada al servidor de Eithne.
  * styles/
    * Hojas de estilo utilizadas para la visualización de la página.
    * style.css
      * Estilo predeterminado.