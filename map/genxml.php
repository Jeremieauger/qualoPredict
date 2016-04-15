<?php
require("dbinfo.php");

function parseToXML($htmlStr)
{
$xmlStr=str_replace('<','&lt;',$htmlStr);
$xmlStr=str_replace('>','&gt;',$xmlStr);
$xmlStr=str_replace('"','&quot;',$xmlStr);
//$xmlStr=str_replace("'",'&#39;',$xmlStr);
$xmlStr=str_replace("&",'&amp;',$xmlStr);
return $xmlStr;
}

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


// Select all the rows in the markers table
$query = 'SELECT i.Station, i.Latitude, i.Longitude, p.UFC, p.Color, i.DescShort FROM `nowPredictions` AS p JOIN `stationInfo` AS i ON p.Station = i.Station;';
$result = mysql_query($query);
if (!$result) {
  die('Invalid query: ' . mysql_error());
}
header("Content-type: text/xml");
// Start XML file, echo parent node
echo '<markers>';
// Iterate through the rows, printing XML nodes for each
while ($row = @mysql_fetch_assoc($result)){
  // ADD TO XML DOCUMENT NODE
  echo '<marker ';
  echo 'name="' . parseToXML($row['Station']) . '" ';
  echo 'lat="' . $row['Latitude'] . '" ';
  echo 'lng="' . $row['Longitude'] . '" ';
  echo 'UFC="' . $row['UFC'] . '" ';
  echo 'Color="' . $row['Color'] . '" ';
  echo 'DescShort="' . parseToXML($row['DescShort']) . '" ';
  echo '/>';
}
// End XML file
echo '</markers>';
?>
