// local variables
const montevideo = ol.proj.fromLonLat([-55.80, -32.50]);
const airport = ol.proj.fromLonLat([-56.028, -34.830]);
const airportId = document.getElementById('center-airport');
const center = document.getElementById('center-map');

// map constructor
const view = new ol.View({
    center: montevideo,
    zoom: 7.1,
  });

var map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM(),
            opacity: 0.9
        }),
    ],
    view: view
});

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