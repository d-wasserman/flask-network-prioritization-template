// Main Application JS File

var map = L.map('map').setView([40.693806, -112.015608], 13);

//Add Base Maps
var stamenAttribution = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'

var Stamen_Toner = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}{r}.{ext}', {
	attribution: stamenAttribution,
	subdomains: 'abcd',
	minZoom: 0,
	maxZoom: 20,
	ext: 'png'
}).addTo(map),
    Stamen_Watercolor = L.tileLayer(
'https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
	attribution: stamenAttribution,
	subdomains: 'abcd',
	minZoom: 0,
	maxZoom: 16,
	ext: 'png'
})
    Esri_WorldTopoMap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
	attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
});

var baseMaps = {
    "Toner": Stamen_Toner,
    "Watercolor": Stamen_Watercolor,
    "Topographic":Esri_WorldTopoMap
    };

L.control.layers(baseMaps).addTo(map);


//Add & Style Network

colorScale = chroma.scale(["ffe760","ff5656","773131"]).domain([1,3]);

function styleColor(feature) {
    return {
        color: colorScale(feature.properties.Priority_Score),
        weight: 3,
        opacity: 1
    };
}

var network = $.getJSON('static/application/data/WestValleyATPNetwork.geojson',function(data){
L.geoJSON(data,{style:styleColor}).addTo(map)});

var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [1,2,3],
        labels = ["Low","Medium","High"],
        title = '<strong> Prioritization Scores </strong>';

    // loop through our density intervals and generate a label with a colored square for each interval
    div.innerHTML= title+ "<br> <br>"
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + colorScale(grades[i]) + '"></i> ' + labels[i] + '<br>';
    }

    return div;
};

legend.addTo(map);


