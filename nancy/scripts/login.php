<?php
	session_start();
	
	require_once "mysql.php";
	require_once "server.php";	

	# Recuperación de variables.
	$username = $_POST['username'];
	$userpass = $_POST['userpass'];
	$database = 'eithne';
	$charset = 'utf8';

	# Validación de variables
	if(is_empty($username) || is_empty($userpass))
	{
		header('Location: index.php?warning=You must enter an user name and a password.');
		exit();
	}

	$link = mysql_connect('localhost', $username, $userpass) or die('Error al conectar: ' . mysql_error());
	mysql_select_db($database, $link) or die('Error al seleccionar base de datos: ' . mysql_error());
	$_SESSION['username'] = $username;
	$_SESSION['userpass'] = $userpass;
	header('Location: ../index.php');
?>
