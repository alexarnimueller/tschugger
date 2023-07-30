// function to create openstreetmap with leaflet
function createMap(elemId, centerLat, centerLng, zoom) {
    var map = new L.Map(elemId);

    // Data provider
    var osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib = 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';

    // Layer
    var osmLayer = new L.TileLayer(osmUrl, {
        minZoom: 2,
        maxZoom: 20,
        attribution: osmAttrib
    });

    // Map
    map.setView(new L.LatLng(centerLat, centerLng), zoom);
    map.addLayer(osmLayer);
    return map;
};

// creating a map with all IAFPA members
document.addEventListener("DOMContentLoaded", function () {
    var map = createMap('map', 47.0, 8.5, 2);
    for ( var i=0; i < members.length; ++i )
    {
       L.marker( [members[i].lat, members[i].lon] )
          .bindPopup( '<a href="' + members[i].url + '" rel="noopener">' + members[i].name + '</a>' )
          .addTo( map );
    };
});