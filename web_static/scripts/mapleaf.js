// local variables
const montevideo = [-32.50, -55.80];
const airport = [-34.833, -56.030];
const airportId = document.getElementById('center-airport');
const center = document.getElementById('center-map');
const collision = document.getElementById('collision');
const totalFlights = document.getElementById('total-flights');
const flights = document.getElementById('flights');
const searchBar = document.getElementById('searchBar');

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
  iconUrl: 'https://images2.imgbox.com/e6/7a/LNpunqi5_o.png',
  iconSize: [30, 30], // size of the icon
  iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
  popupAnchor: [-2, -10], // point from which the popup should open relative to the iconAnchor
  iconId: 'airplane'
});
const airplaneSel = L.icon({
  iconUrl: 'https://images2.imgbox.com/d1/52/akX8YgZ8_o.png',
  iconSize: [30, 30], // size of the icon
  iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
  popupAnchor: [-2, -10], // point from which the popup should open relative to the iconAnchor
  iconId: 'airplane_selected'
});
const airplaneRed = L.icon({
  iconUrl: 'https://images2.imgbox.com/b8/6f/zzFddHpJ_o.png',
  iconSize: [30, 30], // size of the icon
  iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
  popupAnchor: [-2, -10] // point from which the popup should open relative to the iconAnchor
});
L.marker([-34.833, -56.030]).addTo(map).bindTooltip('Carrasco International Airport (SUMU)');

const markers_dict_selected = {};
const route = {};
let markers = new Array();
let polylines = new Array();
let crashes = new Array();
function getPlanes() {
  const json = $.getJSON('flights.json', function (index) {
    if (polylines.length === 0) {
      routeDel();
    }
    totalFlights.innerHTML = Object.keys(index).length;
    const markers_dict = {};
    flights.innerHTML = '';
    const autocomplete = [];
    for (let i = 0; i < Object.keys(index).length; i++) {
      let departure = index[i].departure_ICAO;
      if (departure === "") {
        departure = "N/A"
      }
      let arrival = index[i].arrival_ICAO;
      if (arrival === "") {
        arrival = "N/A"
      }
      flights.innerHTML += '<li class="text-center my-2 rounded flights"> <b>' + index[i].FlightID + '</b></br>' + departure + ' <i class="fas fa-arrow-right me-2"></i>' + arrival + '</li>';
      autocomplete.push(index[i].FlightID);
      const popupOptions =
      {
        'maxWidth': '500',
        'className': 'another-popup' // classname for another popup
      };
      const popupContent = '<h4>Flight ID: ' + index[i].FlightID + '<h4></br><ul class="list-unstyled small"><li>Airline: ' + index[i].airline + '</li><li>Altitude: ' + index[i].path[0].altitude + '</li><li>Speed: ' + index[i].path[0].speed + '</li><li>Truck: ' + index[i].path[0].truck + '</li><li>Departure Airport: ' + index[i].departure_airport + '</li><li>Arrival Time: ' + index[i].arrival_time + '</li><li>Arrival Airport: ' + index[i].arrival_airport + '</li><li>Arrival Time: ' + index[i].arrival_time + '</li></ul>'
      if (!markers_dict_selected[index[i].FlightID]) {
        markers_dict[index[i].FlightID] = index[i];
        markers_dict[index[i].FlightID].status = 'not selected';
        markers_dict[index[i].FlightID].marker = L.marker([index[i].path[0].latitude, index[i].path[0].longitude], { icon: airplane, rotationAngle: index[i].path[0].truck });
        markers_dict[index[i].FlightID].marker.addTo(map).bindTooltip('FlightID: ' + index[i].FlightID).bindPopup(popupContent, popupOptions);
        markers.push(markers_dict[index[i].FlightID].marker);
      } else {
        markers_dict[index[i].FlightID] = index[i];
        markers_dict[index[i].FlightID].status = 'selected';
        markers_dict[index[i].FlightID].marker = L.marker([index[i].path[0].latitude, index[i].path[0].longitude], { icon: airplaneSel, rotationAngle: index[i].path[0].truck });
        markers_dict[index[i].FlightID].marker.addTo(map).bindTooltip('FlightID: ' + index[i].FlightID).bindPopup(popupContent, popupOptions).openPopup();
        markers.push(markers_dict[index[i].FlightID].marker);
        map.removeLayer(markers_dict_selected[index[i].FlightID].route);
        markers.pop(markers_dict_selected[index[i].FlightID].marker);
        markers.pop(markers_dict_selected[index[i].FlightID].route);
        markers_dict[index[i].FlightID].route = L.polyline([[index[i].path[0].latitude, index[i].path[0].longitude], [index[i].estimated_flightpath[1].latitude, index[i].estimated_flightpath[1].longitude]]);
        markers_dict[index[i].FlightID].route.addTo(map);
        polylines.push(markers_dict[index[i].FlightID].route);
        polylines.push(markers_dict_selected[index[i].FlightID].route);
        collision.innerHTML = '';
        if (index[i].collision_l.length > 0) {
          for (let k = 0; k < index[i].collision_l.length; k++) {
            $('#collision').css('color', 'red');;
            console.log(index[i].collision_l);
            collision.innerHTML += '<li>Possible Collission between Aircraft ' + index[i].collision_l[k].ID1 + ' and Aircraft ' + index[i].collision_l[k].ID2 + ' at altitude ' + index[i].collision_l[k].crash_altitude + ' feets</li>';
            markers_dict_selected[index[i].FlightID].crash = L.circle([index[i].collision_l[k].crash_latitude, index[i].collision_l[k].crash_longitude], { radius: 21350, weight: 2, color: '#ff333a', fillColor: '#ff333a' }).addTo(map);
            crashes.push(markers_dict_selected[index[i].FlightID].crash);
          }
        }
      }
      markers_dict[index[i].FlightID].marker.on('click', function onClick(e) {
        if (markers_dict[index[i].FlightID].status == 'not selected') {
          markers_dict[index[i].FlightID].marker.setIcon(airplaneSel);
          markers_dict[index[i].FlightID].status = 'selected';
          markers_dict_selected[index[i].FlightID] = index[i];
          markers_dict_selected[index[i].FlightID].route = L.polyline([[index[i].path[0].latitude, index[i].path[0].longitude], [index[i].estimated_flightpath[1].latitude, index[i].estimated_flightpath[1].longitude]]);
          markers_dict_selected[index[i].FlightID].route.addTo(map);
          polylines.push(markers_dict_selected[index[i].FlightID].route);
          collision.innerHTML = '';
          if (index[i].collision_l.length > 0) {
            for (let k = 0; k < index[i].collision_l.length; k++) {
              $('#collision').css('color', 'red');;
              collision.innerHTML += '<li>Possible Collission between Aircraft ' + index[i].collision_l[k].ID1 + ' and Aircraft ' + index[i].collision_l[k].ID2 + ' at altitude ' + index[i].collision_l[k].crash_altitude + ' feets</li>';
              markers_dict_selected[index[i].FlightID].crash = L.circle([index[i].collision_l[k].crash_latitude, index[i].collision_l[k].crash_longitude], { radius: index[i].collision_l[k].crash_radious * 10, weight: 2, color: '#ff333a', fillColor: '#ff333a' }).addTo(map);
              crashes.push(markers_dict_selected[index[i].FlightID].crash);
            }
          }
        } else {
          crashDel();
          crashes = []
          map.removeLayer(markers_dict_selected[index[i].FlightID].route);
          map.removeLayer(markers_dict[index[i].FlightID].route);
          polylines.pop(markers_dict[index[i].FlightID].route);
          polylines.pop(markers_dict_selected[index[i].FlightID].route);
          delete markers_dict_selected[index[i].FlightID];
          markers_dict[index[i].FlightID].status = 'not selected';
          markers_dict[index[i].FlightID].marker.setIcon(airplane).closePopup();
          $('#collision').css('color', 'rgb(169, 169, 169)');;
          collision.innerHTML = '<li id="collision">Select a plane in the map or in the search bar...</li>';
        }
      });
    }
    $('#flights > li').click(function () {
      const FlightIDLi = $(this).find('b').text();
      if (markers_dict[FlightIDLi].status == 'not selected') {
        markers_dict[FlightIDLi].marker.setIcon(airplaneSel);
        markers_dict[FlightIDLi].status = 'selected';
        markers_dict_selected[FlightIDLi] = markers_dict[FlightIDLi];
        markers_dict_selected[FlightIDLi].route = L.polyline([[markers_dict[FlightIDLi].path[0].latitude, markers_dict[FlightIDLi].path[0].longitude], [markers_dict[FlightIDLi].estimated_flightpath[1].latitude, markers_dict[FlightIDLi].estimated_flightpath[1].longitude]]);
        markers_dict_selected[FlightIDLi].route.addTo(map);
        polylines.push(markers_dict_selected[FlightIDLi].route);
        collision.innerHTML = '';
        if (markers_dict[FlightIDLi].collision_l.length > 0) {
          for (let k = 0; k < markers_dict[FlightIDLi].collision_l.length; k++) {
            $('#collision').css('color', 'red');;
            collision.innerHTML += '<li>Possible Collission between Aircraft ' + markers_dict_selected[FlightIDLi].collision_l[k].ID1 + ' and Aircraft ' + markers_dict_selected[FlightIDLi].collision_l[k].ID2 + ' at altitude ' + markers_dict_selected[FlightIDLi].collision_l[k].crash_altitude + ' feets</li>';
            markers_dict_selected[FlightIDLi].crash = L.circle([markers_dict_selected[FlightIDLi].collision_l[k].crash_latitude, markers_dict_selected[FlightIDLi].collision_l[k].crash_longitude], { radius: markers_dict_selected[FlightIDLi].collision_l[k].crash_radious * 10, weight: 2, color: '#ff333a', fillColor: '#ff333a' }).addTo(map);
            crashes.push(markers_dict_selected[FlightIDLi].crash);
          }
        }
      } else {
        crashDel();
        crashes = []
        map.removeLayer(markers_dict_selected[FlightIDLi].route);
        map.removeLayer(markers_dict[FlightIDLi].route);
        polylines.pop(markers_dict[FlightIDLi].route);
        polylines.pop(markers_dict_selected[FlightIDLi].route);
        delete markers_dict_selected[FlightIDLi];
        markers_dict[FlightIDLi].status = 'not selected';
        markers_dict[FlightIDLi].marker.setIcon(airplane).closePopup();
        $('#collision').css('color', 'rgb(169, 169, 169)');;
        collision.innerHTML = '<li id="collision">Select a plane in the map or in the search bar...</li>';
      }
    });
    searchBar.addEventListener('keyup', (e) => {
      const searchString = e.target.value.toLowerCase();
      let filtered = [];
      if (searchString.length > 0) {
        filtered = autocomplete.filter(flights => {
          return flights.toLowerCase().includes(searchString);
        })
      }
      for (let i = 0; i < filtered.length; i++) {
        //here goes the filter logic
      };
    });
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
  function crashDel() {
    for (i = 0; i < crashes.length; i++) {
      map.removeLayer(crashes[i]);
    }
  }
  markerDel();
  routeDel();
  crashDel();

}
getPlanes();
setInterval(getPlanes, 20000);
//   Center Airport Button
airportId.onclick = function () {
  map.flyTo(airport, 14);
};
//   Center Map Button
center.onclick = function () {
  map.flyTo(montevideo, 7);
};
