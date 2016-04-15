<!DOCTYPE html >
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="stationBS.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCizTuSk3An4_BR836n7XMV4gcgee2HGY0" type="text/javascript"></script>
    <title>Qualo-Pr&eacute;dict</title>
    <script type="text/javascript" src="mapScript.js"></script>
  </head>
<?php
$name = $_GET['name'];
require("dbinfo.php");

function parseToXML($htmlStr)
{
$xmlStr=str_replace('<','&lt;',$htmlStr);
$xmlStr=str_replace('>','&gt;',$xmlStr);
$xmlStr=str_replace('"','&quot;',$xmlStr);
// $xmlStr=str_replace("'",'&#39;',$xmlStr);
$xmlStr=str_replace("&",'&amp;',$xmlStr);
$xmlStr=str_replace("é",'&eacute;',$xmlStr);
$xmlStr=str_replace("è",'&egrave;',$xmlStr);
$xmlStr=str_replace("à",'&agrave;',$xmlStr);
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

// Select all the descriptions from the markers table
$query = "SELECT DescShort, DescLong FROM `stationInfo` WHERE Station='$name';";
// $query = "SELECT Latitude, DescShort FROM `stationInfo`;";
$result = mysql_query($query);
if (!$result) {
  die('Invalid query: ' . mysql_error());
}
while ($row = @mysql_fetch_assoc($result)){
  $descShort = parseToXML($row['DescShort']);
  $descLong = parseToXML($row['DescLong']);
}
// Select the Station names in an ordered list (splitting the name AAA - 111 to order)
$query = "SELECT Station FROM nowPredictions ORDER BY LEFT(Station,LOCATE('-',Station) - 1) , CAST(SUBSTRING(Station,LOCATE('-',Station)+1) AS SIGNED);";
// $query = "SELECT Latitude, DescShort FROM `stationInfo`;";
$result = mysql_query($query);
if (!$result) {
  die('Invalid query: ' . mysql_error());
}
$array = array();
while ($row = @mysql_fetch_assoc($result)){
  $station = $row['Station'];
  array_push($array, $station);
}
$key = array_search($name, $array);
$prevStation = $array[$key-1];
$nextStation = $array[$key+1];
?>

<body>
  <div id="mainMargin">
    <div id="mainBox" class="jumbotron" align="center">
      <div class="row">
        <div class="col-md-3 col-xs-3">
          <a id="prevButton" href="" class="btn btn-info" role="button" style="float:left">
            <span class="glyphicon glyphicon-chevron-left" style="font-size:3vmax"></span>
            <span class="glyphicon glyphicon-chevron-left" style="font-size:3vmax"></span><br>
            <h2><?php echo $prevStation ?></h2>
          </a>
        </div>
        <div class="col-md-6 col-xs-6" style="margin-top:3vmin; margin-bottom:3vmin">
          <div class="btn" style="color: #286090; backgroung-color: inherit">
            <h2 id="homeButton" style="white-space: nowrap"><span class="glyphicon glyphicon-home" style="font-size:3vmax"></span> Retour au site <span class="glyphicon glyphicon-home" style="font-size:3vmax"></span></h2>
          </div>
        </div>
        <div class="col-md-3 col-xs-3">
          <a id="nextButton" href="" class="btn btn-info" role="button" style="float:right">
            <span class="glyphicon glyphicon-chevron-right" style="font-size:3vmax"></span>
            <span class="glyphicon glyphicon-chevron-right" style="font-size:3vmax"></span><br>
            <h2><?php echo $nextStation ?></h2>
          </a>
        </div>
      </div>
      <h1><?php echo $name ?></h1>
      <h2><?php echo $descShort ?></h2>
      <div class="descBox">
        <h3 id="descText"><?php echo $descLong ?></h3>
      </div>
      <div class="imgBox">
        <img class="img-responsive" src="/displayImg.php?name=<?php echo $name . '&type=historical' ?>">
      </div>
      <div class="imgBox">
        <img class="img-responsive" src="/displayImg.php?name=<?php echo $name . '&type=kde' ?>">
      </div>
      <div class="imgBox">
        <img class="img-responsive" src="/displayImg.php?name=<?php echo $name . '&type=seasonal' ?>">
      </div>
      <div class="row">
        <div class="col-md-3 col-xs-3">
          <a id="prevButton2" href="" class="btn btn-info" role="button" style="float:left">
            <span class="glyphicon glyphicon-chevron-left" style="font-size:3vmax"></span>
            <span class="glyphicon glyphicon-chevron-left" style="font-size:3vmax"></span><br>
            <h2><?php echo $prevStation ?></h2>
          </a>
        </div>
        <div class="col-md-6 col-xs-6" style="margin-top:3vmin; margin-bottom:3vmin">
          <div class="btn" style="color: #286090; backgroung-color: inherit">
            <h2 id="homeButton2" style="white-space: nowrap"><span class="glyphicon glyphicon-home" style="font-size:3vmax"></span> Retour au site <span class="glyphicon glyphicon-home" style="font-size:3vmax"></span></h2>
          </div>
        </div>
        <div class="col-md-3 col-xs-3">
          <a id="nextButton2" href="" class="btn btn-info" role="button" style="float:right">
            <span class="glyphicon glyphicon-chevron-right" style="font-size:3vmax"></span>
            <span class="glyphicon glyphicon-chevron-right" style="font-size:3vmax"></span><br>
            <h2><?php echo $nextStation ?></h2>
          </a>
        </div>
      </div>
    </div>
  </div>
</body>
</html>

<script type="text/javascript">
  $(document).ready(function() {
      $("#prevButton").attr('href', "/stationDetails.php?name=<?php echo $prevStation ?>");
      $("#nextButton").attr('href', "/stationDetails.php?name=<?php echo $nextStation ?>");
      $("#homeButton").on("click", function() {
        close();
      });
      $("#prevButton2").attr('href', "/stationDetails.php?name=<?php echo $prevStation ?>");
      $("#nextButton2").attr('href', "/stationDetails.php?name=<?php echo $nextStation ?>");
      $("#homeButton2").on("click", function() {
        close();
      });
      // $("#homeButton").attr('href', "http://<?php echo getenv("OPENSHIFT_APP_DNS"); ?>");
      $("#prevButton2").attr('href', "/stationDetails.php?name=<?php echo $prevStation ?>");
      $("#nextButton2").attr('href', "/stationDetails.php?name=<?php echo $nextStation ?>");
      document.title = "Info - <?php echo $nextStation ?>" ;
    });
</script>
