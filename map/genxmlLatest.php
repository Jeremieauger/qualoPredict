<?php
require("dbinfo.php");
// Open a connection to a MySQL server
$connection = mysql_connect($dbhost.":".$dbport, $dbuser, $passwd);
if (!$connection) {
  die('Not connected : ' . mysql_error());
}
// Set the active MySQL database
$dbconnection = mysql_select_db($dbname);
if (!$dbconnection) {
  die ('Can\'t use db : ' . mysql_error());
}
// Select the time of the predictions
$query = 'SELECT hour, minute FROM `nowPredictions` LIMIT 1;';
$result = mysql_query($query);
if (!$result) {
  die('Invalid query: ' . mysql_error());
}

header("Content-type: text/xml");
// Creating the parent node
echo '<latestPredictions>';
//Iterate to generate the xml element latestPrediction
while ($row = @mysql_fetch_assoc($result)){
  // ADD TO XML DOCUMENT NODE
  echo '<latestPrediction ';
  echo 'hour="' . $row['hour'] . '" ';
  echo 'minute="' . $row['minute'] . '" ';
  echo '/>';
}
echo '</latestPredictions>';
?>
