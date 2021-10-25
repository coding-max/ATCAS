// local variables
const montevideo = [-32.50, -55.80];
const airport = [-34.833, -56.030];
const airportId = document.getElementById('center-airport');
const center = document.getElementById('center-map');
const collision =  document.getElementById('collision');

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
  iconSize:     [30, 30], // size of the icon
  iconAnchor:   [15, 15], // point of the icon which will correspond to marker's location
  popupAnchor:  [-2, -10], // point from which the popup should open relative to the iconAnchor
  iconId: "airplane"
});
const airplaneSel = L.icon({
  iconUrl: './images/airplane_sel.png',
  iconSize:     [30, 30], // size of the icon
  iconAnchor:   [15, 15], // point of the icon which will correspond to marker's location
  popupAnchor:  [-2, -10], // point from which the popup should open relative to the iconAnchor
  iconId: "airplane_selected"
});
const airplaneRed = L.icon({
  iconUrl: './images/airplane_red.png',
  iconSize:     [30, 30], // size of the icon
  iconAnchor:   [15, 15], // point of the icon which will correspond to marker's location
  popupAnchor:  [-2, -10] // point from which the popup should open relative to the iconAnchor
});
L.marker([-34.833, -56.030]).addTo(map).bindPopup("I am an invented airplane.");

async function getPlanes() {
  const json = await $.getJSON('flights.json', function (index) {
    for (let i = 0; i < Object.keys(index).length; i++) {
      const markers = L.marker([index[i].path[0].latitude, index[i].path[0].longitude], { icon: airplane, rotationAngle: index[i].path[0].truck, id: "airplane"}); 
      markers.addTo(map).bindPopup("I am airplane " + index[i].ICAO + " .")
      let flag = true;
      let route = L.polyline([]);
      markers.on("click", function onClick(e) {
        if(markers.options.icon.options.iconId == 'airplane') {
          markers.setIcon(airplaneSel);
          const estimated = [];
          estimated.push([index[i].path[0].latitude, index[i].path[0].longitude]);
          for (let j = 0; j < index[i].estimated_flightpath.length; j++) {
            estimated.push([index[i].estimated_flightpath[j].latitude, index[i].estimated_flightpath[j].longitude]);
          };
          route.remove();
          route = L.polyline(estimated);
          route.addTo(map);
          flag = false;
        } else {
          markers.setIcon(airplane);
          route.remove();
          flag = true;
        }
      });
    }
  });
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
