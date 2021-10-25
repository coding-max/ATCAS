const runway_06 = L.polygon([
  [
    -34.84191525077334,
    -56.03130340576172
  ],
  [
    -34.84191525077334,
    -56.03053092956543
  ],
  [
    -34.82166012434302,
    -56.03053092956543
  ],
  [
    -34.82166012434302,
    -56.03130340576172
  ],
  [
    -34.84191525077334,
    -56.03130340576172
  ]], { color: 'red', stroke: 0 }
);
const runway_01 = L.polygon([
  [
    -34.826592266180164,
    -56.01212024688721
  ],
  [
    -34.843676330629684,
    -56.04022979736328
  ],
  [
    -34.84427508919703,
    -56.039886474609375
  ],
  [
    -34.82705023579321,
    -56.01160526275635
  ],
  [
    -34.826592266180164,
    -56.01212024688721
  ]], { color: 'red', stroke: 0 }
);
  
const sixLabel = document.getElementById("sixLabel");
$(document).ready(function () {
  $('#runwaySix').click(function () {
    if (this.checked) {
      sixLabel.innerHTML = "Disable Runway 06/24";
      runway_06.remove();
    } else {
      map.flyTo(airport, 14);
      sixLabel.innerHTML = "Enable Runway 06/24";
      runway_06.addTo(map);
    };
  })
});
const oneLabel = document.getElementById("oneLabel");
$(document).ready(function () {
  $('#runwayOne').click(function () {
    if (this.checked) {
      oneLabel.innerHTML = "Disable Runway 01/19";
      runway_01.remove();
    } else {
      map.flyTo(airport, 14);
      oneLabel.innerHTML = "Enable Runway 01/19";
      runway_01.addTo(map)
    };
  });
});