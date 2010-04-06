<?php

function make_header($title)
{
	echo "
<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 //EN' 'http://www.w3c.org/TR/html4/strict.dtd'>
<HTML>
	<HEAD>
		<META http-equiv='Content-Type' content='text/html;charset=utf-8'>
		<META http-equiv='Content-Script-Type' content='text/javascript'>
		<SCRIPT type='text/javascript' src='scripts/client.js' charset='utf-8'></SCRIPT>
		<LINK rel='stylesheet' type='text/css' charset='utf-8' media='screen' href='styles/style.css' title='Main'>
		<TITLE>$title</TITLE>
	</HEAD>

	<BODY>
	<DIV id='body'>
		<DIV id='title'>
			<BR>
			<H1><A class='logo' href='index.php'>Eithne's Fancy Reporting System (Nancy)</A></H1>
			<BR>
		</DIV>
	";

	if (isSet($_SESSION['username']))
	{
		echo "<P>Logged as ".$_SESSION['username'].". <A href='scripts/logout.php'>Logout</A></P>";
	}
}

function make_footer()
{
	echo "
		<DIV id='footer'>
			<A class='footer' href='index.php'></A>
			<BR><DIV id='title'><BR></DIV><BR>
		</DIV>
	</DIV>
	</BODY>
</HTML>
	";
}

function make_index($username)
{
	switch ($username)
	{
		case '':
			$warning = $_GET['warning'];
			if ($warning != "")
				echo "<P class='red'>$warning</P>\n";
			echo "<P class='center'>User name and password to connect database:</p>\n";
			# Formulario de login ----------------------------------------
			echo "<FORM onsubmit='return (notEmpty(this.username) && notEmpty(this.userpass))' action='scripts/login.php' method='post'>\n";
			echo "<TABLE align='center' border='0'>\n";
			echo "<TR>\n";
			echo "<TD><LABEL for='username'>User name: </LABEL></TD>\n";
			echo "<TD><INPUT id='username' name='username' type='text' size='9' maxlength='9'></TD>\n";
			echo "</TR><TR>\n";
			echo "<TD><LABEL for='userpass'>Password: </LABEL></TD>\n";
			echo "<TD><INPUT id='userpass' name='userpass' type='password' size='9' maxlength='12'></TD>\n";
			echo "</TR><TR>\n";
			echo "<TD><BUTTON type='submit'>Submit</BUTTON>\n";
			echo "<TD><BUTTON type='reset'>Reset</BUTTON>\n";
			echo "</TR></TABLE>\n";
			echo "</FORM>\n";
			# ------------------------------------------------------------
			break;
		
		default:
			$IDNet = $_GET['IDNet'];
			if ($IDNet == '')
			{
				$IDNet = '0';
			}
			$IDCom = $_GET['IDCom'];
			if ($IDCom == '')
			{
				$IDCom = '0';
			}
			$username = $_SESSION['username'];
			$userpass = $_SESSION['userpass'];
			$database = 'eithne';
			$charset = 'utf8';
			$link = connectDatabase($database, $username, $userpass, $charset);
			$query = "select IDNet, Name from NETWORKS order by Name";
			$networks = sendQuery($query, $link);
			$query = "select IDCom, Name from COMPUTERS inner join MEMBERS on Computer=IDCom where Network=".$IDNet;
			$computers = sendQuery($query, $link);
			if (mysql_num_rows($networks) == 0)
			{
				echo "<P class='red'>No networks registered.</P>\n";
			}
			else
			{
				$num_net = mysql_num_rows($networks);
				$num_com = mysql_num_rows($computers);
				if ($num_net > $num_com)
				{
					$n = $num_net;
				}
				else
				{
					$n = $num_com;
				}
				echo "<TABLE align='center'border='0'>\n";
				echo "<TR><TD class='main'>\n";
				echo "<TABLE id='select' class='list' align='center' border='0'>\n";
				echo "<TR><TH>Networks</TH><TH>Computers</TH></TR>\n";
				for ($i=0; $i<$n ;$i++)
				{
					$net_row = mysql_fetch_array($networks, MYSQL_ASSOC);
					$com_row = mysql_fetch_array($computers, MYSQL_ASSOC);

					echo "<TR>\n";

					# Columna de las redes.
					if ($net_row['IDNet'] == $IDNet)
					{
						echo "<TD class='current_net'>";
					}
					else echo "<TD class='net'>";
					echo "<A class='network' href='index.php?IDNet=".$net_row['IDNet']."'>".$net_row['Name']."</A></TD>\n";

					# Columna de los equipos.
					if ($com_row['IDCom'] == $IDCom)
					{
						echo "<TD class='current_com'>";
					}
					else echo "<TD class='com'>";
					echo "<A class='computer' href='index.php?IDNet=".$IDNet."&IDCom=".$com_row['IDCom']."'>".$com_row['Name']."</A></TD>\n";
		
					echo "</TR>\n";
				}
				echo "</TABLE>\n";
				echo "</TD>\n";

				echo "<TD class='main'>\n";
				echo "<FORM id='show' onsubmit='alert(\"Paso del tema.\"); return false' action='scripts/send_request.php' method='GET'>\n";
				echo "<TABLE align='center' border='0'>\n";
				echo "<TR>\n";
				echo "<TH>Show</TH>\n";
				echo "</TR><TR>\n";
				if ($IDCom != '0')
				{
					echo "<TD><LABEL for='cpu'>CPU </LABEL></TD>\n";
					echo "<TD><INPUT id='cpu' name='cpu' type='checkbox' checked></TD>\n";
					echo "</TR><TR>\n";
					echo "<TD><LABEL for='memory'>Memory </LABEL></TD>\n";
					echo "<TD><INPUT id='memory' name='memory' type='checkbox' checked></TD>\n";
					echo "</TR><TR>\n";
					echo "<TD><LABEL for='storage'>Storage </LABEL></TD>\n";
					echo "<TD><INPUT id='storage' name='storage' type='checkbox' checked></TD>\n";
					echo "</TR><TR>\n";
					echo "<TD><A target='_blank' href='http://localhost:8000/".$IDNet."/".$IDCom."'>Full Report</A></TD>\n";
					echo "</TR><TR>\n";
					echo "<TD><BUTTON type='submit'>Submit</BUTTON>\n";
					echo "<TD><BUTTON type='reset'>Reset</BUTTON>\n";
				}
				else
				{
					echo "<TD><P class='red'>Select a computer</P></TD>\n";
				}
				echo "</TR></TABLE>\n";
				echo "</FORM>\n";
				echo "</TD></TR>\n";
				echo "</TABLE>\n";
			}
			break;
	}
}


?>
