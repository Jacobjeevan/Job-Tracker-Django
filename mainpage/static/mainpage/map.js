var map = new mapboxgl.Map({
  container: "map",
  center: map_center,
  style: "mapbox://styles/mapbox/light-v10",
  zoom: zoom,
});

function getPopup(job) {
  return new mapboxgl.Popup({
    offset: 25,
    closeOnMove: true,
    closeButton: false,
  }).setText(`${job.properties.description}`);
}

function createDivElement() {
  var element = document.createElement("div");
  element.className = "marker";
  element.style.backgroundImage =
    "url(https://job-tracker.s3.amazonaws.com/job.png)";
  element.style.width = "20px";
  element.style.height = "20px";
  return element;
}

/* function createPopupEvents(element, marker, popup) {
    element.addEventListener('mouseenter', function () {
        marker.setPopup(popup)
        marker.togglePopup()
    });
    element.addEventListener('mouseleave', function () {
        popup.remove()
    });

} */

geojson.features.forEach(function (job) {
  var element = createDivElement();
  var popup = getPopup(job);
  var marker = new mapboxgl.Marker(element)
    .setLngLat(job.geometry.coordinates)
    .addTo(map)
    .setPopup(popup);
  // createPopupEvents(element, marker, popup)
});
