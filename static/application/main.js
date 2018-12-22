// Main Application JS File

var map = L.map('map').setView([40.693806, -112.015608], 13);

var Stamen_Toner = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}{r}.{ext}', {
	attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
	subdomains: 'abcd',
	minZoom: 0,
	maxZoom: 20,
	ext: 'png'
}).addTo(map);

colorScale = chroma.scale(["yellow","red","darkred"]).domain([1,3]);

function styleColor(feature) {
    return {
        color: colorScale(feature.properties.Priority_Score),
        weight: 3,
        opacity: 1
    };
}

$.getJSON('static/application/data/WestValleyATPNetwork.geojson',function(data){
L.geoJSON(data,{style:styleColor}).addTo(map)});

var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [1,2,3],
        labels = ["Low","Medium","High"];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + colorScale(grades[i]) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);
