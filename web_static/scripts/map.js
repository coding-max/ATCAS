// local variables
const montevideo = ol.proj.fromLonLat([-55.80, -32.50]);
const airport = ol.proj.fromLonLat([-56.030, -34.833]);
const airportId = document.getElementById('center-airport');
const center = document.getElementById('center-map');
const attribution = new ol.control.Attribution({
  collapsible: false
});
// Airplanes+
const json = [{
    "FlightID": "E480D1", 
    "IATA": "", 
    "ICAO": "TAM8132", 
    "airline": "", 
    "arrival_IATA": "", 
    "arrival_ICAO": "", 
    "arrival_airport": "", 
    "arrival_time": "0000-00-00 00:00:00", 
    "collision_l": [], 
    "current_path": 0, 
    "departure_IATA": "", 
    "departure_ICAO": "", 
    "departure_airport": "", 
    "departure_time": "0000-00-00 00:00:00", 
    "estimated_flightpath": [
      {
        "altitude": 31225, 
        "latitude": -33.84468411009274, 
        "longitude": -57.33153381202181, 
        "speed": 393, 
        "time": "2021-10-20t16:27:00z", 
        "truck": 224
      }, 
      {
        "altitude": 31225, 
        "latitude": -34.56494268155804, 
        "longitude": -58.17276153505804, 
        "speed": 393, 
        "time": "2021-10-20T16:38:20Z", 
        "truck": 224
      }
    ], 
    "manifesto": false, 
    "path": [
      {
        "altitude": 31225, 
        "latitude": -33.8235, 
        "longitude": -57.3069, 
        "speed": 393, 
        "time": "2021-10-20T16:26:40Z", 
        "truck": 224
      }
    ], 
    "registration": "PR-MHP", 
    "status": "On air", 
    "suggested_flightpath": [], 
    "type": "A320", 
    "working_altitude": 14
}];

// map constructor
const view = new ol.View({
    center: montevideo,
    zoom: 7.1,
});

var map = new ol.Map({
    controls: ol.control.defaults({attribution: false}).extend([attribution]),
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM({
              attributions: [ ol.source.OSM.ATTRIBUTION, 'Map Propietry of ©<a href="#">ATCAS</a>' ],
            }),
            opacity: 0.9
        }),
    ],
    view: view
});


// a vector layer to render the source
let vector;
function reload() {
  var vectorSource = new ol.source.Vector({
    url: 'flights.geojson',
    format: new ol.format.GeoJSON(),
  });
  var newLayer = new ol.layer.Vector({
    source: vectorSource,
  });
  map.addLayer(newLayer);
  // vectorSource.once('change', function(){
  //   if(vector) {
  //     map.removeLayer(vector);
  //   }
  //   vector = newLayer;
  //   var propietries = vectorSource.getFeatures();
  //   propietries.forEach(element => {
  //     rot = element.get('rotation');
  //   });
  // });
  //styling the vector
  const iconStyle = new ol.style.Style({
    image: new ol.style.Icon({
      anchor: [0.5, 0.5],
      src: './images/airplane_1.png',
      scale: 0.5,
      rotation: 120
    }),
  });
  newLayer.setStyle(iconStyle);
}
reload();
window.setInterval(reload, 10000);


// Fly Animation
function flyTo(scale, location, done) {
    const duration = 1500;
    const zoom = view.getZoom();
    let parts = 2;
    let called = false;
    function callback(complete) {
      --parts;
      if (called) {
        return;
      }
      if (parts === 0 || !complete) {
        called = true;
        done(complete);
      }
    };
    view.animate(
      {
        center: location,
        duration: duration,
      },
      callback
    );
    view.animate(
      {
        zoom: zoom - 1,
        duration: duration / 2,
      },
      {
        zoom: scale,
        duration: duration / 2,
      },
      callback
    );
};

//   Center Airport Button
airportId.onclick = function () {
    flyTo(14, airport, function () {});
};
//   Center Map Button
center.onclick = function () {
    flyTo(7.1, montevideo, function () {});
};
