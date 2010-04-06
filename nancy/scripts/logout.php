<?php
	session_start();

	if (!isSet($_SESSION['username']))
	{
		header('Location: ../index.php');
		exit();
	}
	else
	{	
		session_destroy();
		header('Location: ../index.php');
	}
?>
	
