// Main Application JS File

//Jquery Ready
$( document ).ready(function() {
  console.log( 'Document Ready' );
});

//Establish Key Variables/Const
const filePath = "static/application/data/WestValleyATPNetwork.geojson"; //Use for static reference
const serviceURL = "api/network_geojson.geojson"; // Use for dynamic weighted reference
var valueDomains = [1,3]
var colorSpectrum = ["ffe760","ff5656","773131"]
var networkOptions = {style:styleColor,onEachFeature:setupPopUp}
//Set Up Map Basic

var map = L.map('map').setView([40.688, -112.00], 13);

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

colorScale = chroma.scale(colorSpectrum).domain(valueDomains);

function styleColor(feature) {
    return {
        color: colorScale(feature.properties.Priority_Score),
        weight: 3,
        opacity: 1
    };
}

var customPopUpOptions =
        {
        'maxWidth': '500',
        'className' : 'customPopUp'
        }

function setupPopUp(f,l){
    var out = [];
    if (f.properties){
        for(key in f.properties){
            out.push(key+": "+f.properties[key]);
        }
        l.bindPopup(out.join("<br />"),customPopUpOptions);
    }
}

var networkLayer = new L.GeoJSON.AJAX(serviceURL,networkOptions);
networkLayer.addTo(map);
//Legend
var legend = L.control({position: 'bottomright'});



legend.onAdd = function (map) {

var div = L.DomUtil.create('div', 'info legend'),
    grades = [1,2,3],
    labels = ["Low","Medium","High"],
    title = '<h6><strong> Prioritization Scores </strong></h6>';

div.innerHTML=  title + "<br>"
for (var i = 0; i < grades.length; i++) {
    div.innerHTML +=
        '<i style="background:' + colorScale(grades[i]) + '"></i> ' + '<h6 class="legendText">' + labels[i] + '</h6>' + '<br>';
}
    return div;
};

legend.addTo(map);

// Create Sum of Elements
 
function recomputeWeightedSum(){
	var sliderOutputSum = 0;
	$(".output").each(function(){
		sliderOutputSum += parseFloat($(this).text());
		return sliderOutputSum
	});
	$("h6.sliderTotalSum").text(sliderOutputSum.toFixed(2)).append(" %"); 
};

recomputeWeightedSum(); //Initial Set up
$(".slider").change(recomputeWeightedSum); // On Change