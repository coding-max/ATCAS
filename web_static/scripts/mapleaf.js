// local variables
const montevideo = [-32.50, -55.80];
const airport = [-34.833, -56.030];
const airportId = document.getElementById('center-airport');
const center = document.getElementById('center-map');
const collision = document.getElementById('collision');
const totalFlights = document.getElementById('total-flights');
const flights = document.getElementById('flights');


// map constructor
var map = L.map('mapid').setView(montevideo, 7);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="#">OpenStreetMap</a> contributors, Map Propietry of &copy <a href="#">ATCAS</a>',
  maxZoom: 18,
  opacity: 0.8,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: 'pk.eyJ1IjoidG9zaGliIiwiYSI6ImNrdjJqMzh4aTBjNTYybnA2OHAzNXl4em0ifQ.SRtHX1Z6ziF7babo6wfVtA'
}).addTo(map);

// Icon Creation
const airplane = L.icon({
  iconUrl: './images/airplane_1.png',
  iconSize: [30, 30], // size of the icon
  iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
  popupAnchor: [-2, -10], // point from which the popup should open relative to the iconAnchor
  iconId: 'airplane'
});
const airplaneSel = L.icon({
  iconUrl: './images/airplane_sel.png',
  iconSize: [30, 30], // size of the icon
  iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
  popupAnchor: [-2, -10], // point from which the popup should open relative to the iconAnchor
  iconId: 'airplane_selected'
});
const airplaneRed = L.icon({
  iconUrl: './images/airplane_red.png',
  iconSize: [30, 30], // size of the icon
  iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
  popupAnchor: [-2, -10] // point from which the popup should open relative to the iconAnchor
});
L.marker([-34.833, -56.030]).addTo(map).bindTooltip('Carrasco International Airport (SUMU)');

const markers_dict_selected = {};
const route = {};
let markers = new Array();
let polylines = new Array();
function getPlanes() {
  const json = $.getJSON('flights.json', function (index) {
    if (polylines.length === 0){
      routeDel();
    }
    totalFlights.innerHTML = Object.keys(index).length;
    const markers_dict = {};
    flights.innerHTML = '';
    for (let i = 0; i < Object.keys(index).length; i++) {
      flights.innerHTML += '<li class="text-center my-2 rounded flights"> <b>' + index[i].FlightID + '</b></br>'+ index[i].departure_airport + ' <i class="fas fa-arrow-right me-2"></i>' + index[i].arrival_airport + '</li>';
      if (!markers_dict_selected[index[i].FlightID]) {
        markers_dict[index[i].FlightID] = index[i];
        markers_dict[index[i].FlightID].status = 'not selected';
        markers_dict[index[i].FlightID].marker = L.marker([index[i].path[0].latitude, index[i].path[0].longitude], { icon: airplane, rotationAngle: index[i].path[0].truck });
        markers_dict[index[i].FlightID].marker.addTo(map).bindTooltip('FlightID: ' + index[i].FlightID).bindPopup('HOLA');
        markers.push(markers_dict[index[i].FlightID].marker);
      } else {
        markers_dict[index[i].FlightID] = index[i];
        markers_dict[index[i].FlightID].status = 'selected';
        markers_dict[index[i].FlightID].marker = L.marker([index[i].path[0].latitude, index[i].path[0].longitude], { icon: airplaneSel, rotationAngle: index[i].path[0].truck });
        markers_dict[index[i].FlightID].marker.addTo(map).bindTooltip('FlightID: ' + index[i].FlightID).bindPopup('HOLA').openPopup();
        markers.push(markers_dict[index[i].FlightID].marker);
        map.removeLayer(markers_dict_selected[index[i].FlightID].route);
        markers.pop(markers_dict_selected[index[i].FlightID].marker);
        markers_dict[index[i].FlightID].route = L.polyline([[index[i].path[0].latitude, index[i].path[0].longitude], [index[i].estimated_flightpath[1].latitude, index[i].estimated_flightpath[1].longitude]]);
        markers_dict[index[i].FlightID].route.addTo(map);
        polylines.push(markers_dict[index[i].FlightID].route);
        polylines.push(markers_dict_selected[index[i].FlightID].route);
      }
      markers_dict[index[i].FlightID].marker.on('click', function onClick(e) {
        if (markers_dict[index[i].FlightID].status == 'not selected') {
          markers_dict[index[i].FlightID].marker.setIcon(airplaneSel);
          markers_dict[index[i].FlightID].status = 'selected';
          markers_dict_selected[index[i].FlightID] = index[i];
          markers_dict_selected[index[i].FlightID].route = L.polyline([[index[i].path[0].latitude, index[i].path[0].longitude], [index[i].estimated_flightpath[1].latitude, index[i].estimated_flightpath[1].longitude]]);
          markers_dict_selected[index[i].FlightID].route.addTo(map);
          polylines.push(markers_dict[index[i].FlightID].route);
          polylines.push(markers_dict_selected[index[i].FlightID].route);
          collision
        } else {
          map.removeLayer(markers_dict_selected[index[i].FlightID].route);
          map.removeLayer(markers_dict[index[i].FlightID].route);
          polylines.pop(markers_dict[index[i].FlightID].route);
          polylines.pop(markers_dict_selected[index[i].FlightID].route);
          delete markers_dict_selected[index[i].FlightID];
          markers_dict[index[i].FlightID].status = 'not selected';
          markers_dict[index[i].FlightID].marker.setIcon(airplane).closePopup();
        }
      });
    }
  });
  function markerDel() {
    for (i = 0; i < markers.length; i++) {
      map.removeLayer(markers[i]);
    }
  }
  function routeDel() {
    for (i = 0; i < polylines.length; i++) {
      map.removeLayer(polylines[i]);
    }
  }
  markerDel();
  routeDel()
}
getPlanes();
setInterval(getPlanes, 10000);
//   Center Airport Button
airportId.onclick = function () {
  map.flyTo(airport, 14);
};
//   Center Map Button
center.onclick = function () {
  map.flyTo(montevideo, 7);
};
