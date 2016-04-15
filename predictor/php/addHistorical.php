<?php
require("dbinfo.php");

$dir_path = getenv("OPENSHIFT_REPO_DIR");
$dir_path = $dir_path . "php/historical/";
$dir_handle = opendir($dir_path);

// Opens a connection to a MySQL server
$connection = mysql_connect($dbhost.":".$dbport, $dbuser, $passwd);
if (!$connection) {
  die('Not connected : ' . mysql_error());
}
// Set the active MySQL database
$dbconnection = mysql_select_db($dbname);
if (!$dbconnection) {
  die ('Can\'t use db : ' . mysql_error());
}

while ($filename = readdir($dir_handle))
{
	if ($filename == '.' || $filename == '..')
	{
		continue;
	}
	$filenameFULL = $dir_path . $filename;
	$imgData = file_get_contents($filenameFULL);
	$nameSimple = substr($filename, 0, -4);

	$sql = sprintf("INSERT INTO PNG
		(Station, Type, Year, graph)
		VALUES 
		('%s', '%s', '%s', '%s') 
		ON DUPLICATE KEY UPDATE graph='%s'",
		$nameSimple,
		'historical',
		'000',
		mysql_real_escape_string($imgData),
		mysql_real_escape_string($imgData)
		);
	mysql_query($sql);
}
?>