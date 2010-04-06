<?php
	session_start();

	require_once "scripts/functions.php";
	require_once "scripts/mysql.php";
	
	make_header("Eithne's Fancy Reporting System - Nancy");

	if (isSet($_SESSION['username']))
	{
		make_index($_SESSION['username']);
	}
	else
	{
		make_index('');
	}
	make_footer();
	?>
