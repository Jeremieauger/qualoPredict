<?php
$name = $_GET['name'];
$type = $_GET['type'];
require("dbinfo.php");

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

$sql = "SELECT graph FROM `PNG` WHERE Station='$name' AND Type='$type'";
$result = mysql_query("$sql");
$row = mysql_fetch_assoc($result);
mysql_close($link);
header("Content-type: image/png");
echo $row['graph'];
?>
