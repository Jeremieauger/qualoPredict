// based on "https://developers.google.com/maps/articles/phpsqlajax_v3#domfunctions" and "https://github.com/googlemaps/js-samples/tree/gh-pages/articles/phpsqlajax"
function load() {
  var map = new google.maps.Map(document.getElementById("map"), {
    center:new google.maps.LatLng(45.555891, -73.703381),
    zoom: 10,
    disableDefaultUI: true,
    mapTypeControl: true,
    mapTypeControlOptions: {
      position: google.maps.ControlPosition.TOP_RIGHT,
      mapTypeIds: [
        google.maps.MapTypeId.SATELLITE,
        google.maps.MapTypeId.HYBRID,
        google.maps.MapTypeId.ROADMAP
      ]
    },
    mapTypeId: 'roadmap'
  });

  map.controls[google.maps.ControlPosition.LEFT_TOP].push(graphLegend);
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(placeHolder);
  map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(staticLegend);
  map.controls[google.maps.ControlPosition.RIGHT_TOP].push(homeButton);
  map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(smallLegend);

  downloadUrl("genxmlLatest.php", function(data) {
    var xml = data.responseXML;
    var latestPredictions = xml.documentElement.getElementsByTagName("latestPrediction");
    var hour = latestPredictions[0].getAttribute("hour");
    var minute = latestPredictions[0].getAttribute("minute");
    $("#latestPrediction").html('Pr&eacute;dit &agrave;: '+hour+'h'+minute);
  });

  var infoWindow = new google.maps.InfoWindow;
  downloadUrl("genxml.php", function(data) {
    var bounds = new google.maps.LatLngBounds();
    var xml = data.responseXML;
    var markers = xml.documentElement.getElementsByTagName("marker");
    for (var i = 0; i < markers.length; i++) {
      var name = markers[i].getAttribute("name");
      var predUFC = markers[i].getAttribute("UFC");
      var color = markers[i].getAttribute("Color");
      var DescShort = markers[i].getAttribute("DescShort");
      var point = new google.maps.LatLng(
          parseFloat(markers[i].getAttribute("lat")),
          parseFloat(markers[i].getAttribute("lng")));
      bounds.extend(point);
      var marker = new google.maps.Marker({
        map: map,
        position: point,
        optimized: false,
        zIndex: parseInt(predUFC),
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: 3.5,
          strokeColor: color,
          strokeOpacity: 0.9,
          strokeWeight: 10,
          fillColor: color,
          fillOpacity: 1
        }
      });
      bindInfoWindow(marker, map, infoWindow, name, color, predUFC, DescShort);
    }
    map.fitBounds(bounds);
    var currentCenter = map.getCenter();
    var currentZoom = map.getZoom();
    map.addListener('center_changed', function() {
      setTimeout(function myFunction() {
        currentCenter = map.getCenter();
        currentZoom = map.getZoom();
      }, 5);
    });
    map.addListener('zoom_changed', function() {
      setTimeout(function myFunction() {
        currentCenter = map.getCenter();
        currentZoom = map.getZoom();
      }, 5);
    });
    google.maps.event.addDomListener(window, "resize", function() {
      map.setZoom(currentZoom);
      map.setCenter(currentCenter);
    });
    google.maps.event.addDomListener(window, "orientationchange", function() {
      map.setZoom(currentZoom);
      map.setCenter(currentCenter);
    });
    $("#homeButton").on("click", function() {
      map.fitBounds(bounds);
    });
  });
}

function bindInfoWindow(marker, map, infoWindow, name, color, predUFC, DescShort) {
  google.maps.event.addListener(marker, 'click', function() {
    $('#placeHolder').hide();
    $('#graphLegend').show();
    $("#predName").html('<h1>'+name+'</h1><h2>'+DescShort+'</h2>');
    $("#detailsLink").attr('href', '/stationDetails.php?name=' + name);
    $("#detailsLink").css('background-color', color)
    $("#predUFC").html(predUFC);
    $("#predNum").html(calcNum(predUFC));
    $("#predString").html(calcString(predUFC));
    $('#graph').attr('src', '/displayImg.php?type=historical&name=' + name);
    $("#graphLink").on("click", function() {
       $('#imagepreview').attr('src', $('#graph').attr('src')); // here asign the image to the modal when the user click the enlarge link
       $('#imagemodal').modal('show'); // imagemodal is the id attribute assigned to the bootstrap modal, then i use the show function
    });
  });
  google.maps.event.addListener(marker, 'mouseover', function() {
    infoWindow.setContent('<h3>' + DescShort + '</h3>');
    infoWindow.open(map, marker);
  });
  google.maps.event.addListener(marker, 'mouseout', function() {
    infoWindow.close();
  });
  google.maps.event.addListener(marker, 'dblclick', function() {
    map.setCenter(marker.position);
    map.setZoom(map.getZoom()+2);
  });
  $(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
  });
}

function downloadUrl(url, callback) {
  var request = window.ActiveXObject ?
      new ActiveXObject('Microsoft.XMLHTTP') :
      new XMLHttpRequest;

  request.onreadystatechange = function() {
    if (request.readyState == 4) {
      request.onreadystatechange = doNothing;
      callback(request, request.status);
    }
  };
  request.open('GET', url, true);
  request.send(null);
}

function doNothing() {}

function calcNum(predUFC) {
  var predNum = 9999;
  if (predUFC < 200){
    predNum = 1;
  }
  if (predUFC >= 200 && predUFC < 1000){
    predNum = 2;
  }
  if (predUFC >= 1000){
    predNum = 3;
  }
  return predNum;
}
function calcString(predUFC) {
  var predString = 9999;
  if (predUFC < 200){
    predString = 'Baignade permise';
  }
  if (predUFC >= 200 && predUFC < 1000){
    predString = 'Activit&eacute;s sans contact';
  }
  if (predUFC >= 1000){
    predString = 'Activit&eacute;s interdites';
  }
  return predString;
}
