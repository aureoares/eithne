<?php
	# Conecta con una base de datos y establece las variables de sesión.
	function connectDatabase($database, $username, $userpass, $charset)
	{

		# Conecto con la base de datos.
		$link = mysql_connect('localhost', $username, $userpass) or die('Cannot connect database.');

		mysql_select_db($database, $link) or die('No database selected.');
		
		# Establezco el charset del cliente.
		$query = 'set character_set_client = '.$charset;
		$result = sendQuery($query, $link);
		$query = 'set character_set_results = '.$charset;
		$result = sendQuery($query, $link);
		
		# Averiguo el charset de la base de datos.
		$query = "show variables where Variable_name='character_set_database'";
		$result = sendQuery($query, $link);
		$row = mysql_fetch_array($result, MYSQL_ASSOC);
		$database_charset = $row['Value'];
		$query = 'set character_set_connection = '.$database_charset;
		$result = sendQuery($query, $link);

		return $link;
	}
	
	# Cierra la conexión con una base de datos.
	function disconnectDatabase($link)
	{
		mysql_close($link) or die(mysql_error());
	}

	# Realiza una consulta.
	function sendQuery($query, $link)
	{			
		$result = mysql_query($query, $link) or die(mysql_error());
		return $result;
	}
?>
