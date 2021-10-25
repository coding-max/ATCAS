const sixLabel = document.getElementById("sixLabel");
$(document).ready(function () {
    $('#runwaySix').click(function () {
      if (this.checked) {
          sixLabel.innerHTML = "Disable Runway 06/24";
        } else {
          sixLabel.innerHTML = "Enable Runway 06/24";
      };
    })
});

const oneLabel = document.getElementById("oneLabel");
$(document).ready(function () {
    $('#runwayOne').click(function () {
      if (this.checked) {
          oneLabel.innerHTML = "Disable Runway 01/19";
        } else {
        oneLabel.innerHTML = "Enable Runway 01/19";
      };
    })
});