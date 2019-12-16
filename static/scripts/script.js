// The following file contains all the scripts for the website

// The constant centerPosition marks the central location of the map
// In this case it has the coordinates for Aarhus' center.
const centerPosition = { lat: 56.162939, lng: 10.203921 };
var map;
var markers = [];
var bicycles = [];
var icon = {url:'/static/icons/bike-icon.png'};


// The function set Markers will set markers on the database coordinates.
// It takes one argument: bicycles. Which is an array of coordinates.
function setMarkers(bicycles) {
    // First it calls our function that gets the coordinate values
    getAllCoordinates();

    for (var i = 0; i < bicycles.length; i++) {
      // The array bicycles is multidimentional, so we extract the respective coordinate array
      var bicycle = bicycles[i];
      // The object myLatLng is a reformated version of the bicycle array, in a way that is
        // compatible with GoogleMaps
      var myLatLng = new google.maps.LatLng(parseFloat(bicycle[1]), parseFloat(bicycle[2]));
      // A new marker is created with the previously defined map, icon, latitude and longitude.
      var marker = new google.maps.Marker({
      map: map,
      position: myLatLng,
      icon: icon,
      zIndex: Number(bicycle[2])
    });
    // add the new marker to the markers array.
    markers.push(marker);
  }
}

// The function reloadMarkers deletes all the previous markers and generates new ones.
function reloadMarkers() {
    for (var i=0; i<markers.length; i++) {
        markers[i].setMap(null);
    }

    markers = [];

    setMarkers(bicycles);
}

// The function init is a callback function called when the map is created on the index.html page
function init() {
  // create the map with the centerPosition constant
  map = new google.maps.Map(document.getElementById('map'), {
    center: centerPosition,
    zoom: 11
  });
  // set the first markers
  setMarkers(bicycles);
  // every second reload the markers
  window.setInterval(reloadMarkers, 1000);
}

// function to get all the database's coordinates
function getAllCoordinates() {
    // Using ajax, we create a request to the /coordinates endpoint.
    // The response is reformated so it can be used by our program to create markers.
    jQuery.ajax({
        url: '/coordinates',
        type: 'get',
        success: function(response) {
            var bikearray = response.split("-B");
            bicycles = [];
            for(i = 0; i < bikearray.length - 1; i++) {
                var bike = bikearray[i];
                bicycles.push(bike.split(", "));
            }
            return(bicycles);
        }
    });
}