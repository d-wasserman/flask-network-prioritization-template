// Main Application JS File

//Jquery Ready
$( document ).ready(function() {
  console.log( 'Document Ready' );
});

//Establish Key Variables/Const
const filePath = "static/application/data/WestValleyATPNetwork.geojson"; //Use for static reference
const serviceURL = "api/network_geojson.geojson"; // Use for dynamic weighted reference
var valueDomains = [1,3]
var differenceDomains = [-1,1]
var priorityColorSpectrum = ["ffe760","ff5656","773131"]
var differenceColorSpectrum = ["67a9cf","f7f7f7","ef8a62"]
var priorityOptions = {style:priorityColor,onEachFeature:setupPopUp}
var differenceOptions = {style:differenceColor,onEachFeature:setupPopUp}
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


//Style Network

priorityColorScale = chroma.scale(priorityColorSpectrum).domain(valueDomains);
differenceColorScale = chroma.scale(differenceColorSpectrum).domain(differenceDomains);
function priorityColor(feature) {
    return {
        color: priorityColorScale(feature.properties.Priority_Score),
        weight: 3,
        opacity: 1
    };
}
function differenceColor(feature) {
    return {
        color: differenceColorScale(feature.properties.Difference_Score),
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

// Add Network & Refresh
var priorityLayer = new L.GeoJSON.AJAX(serviceURL,priorityOptions);
var differenceLayer = new L.GeoJSON.AJAX(serviceURL,differenceOptions);

priorityLayer.addTo(map);

function refreshGeojson(){
	var new_weights = {};
	$(".slider").each(function(){
		new_weights[this.name]=this.value;
	});
	console.log(new_weights)
	req = $.ajax({
		url:"/revise_weights",
		type: "POST",
		data: new_weights,
		// send data to revised weights url - function 
		// will read form on back end
	});
	req.done(function(data){
		priorityLayer.refresh();
		differenceLayer.refresh();
		console.log("Refreshed Layers.");
		// When Done, refresh the geojson. 
	});
	
};

// Layer Control 
var baseMaps = {
    "Toner": Stamen_Toner,
    "Watercolor": Stamen_Watercolor,
    "Topographic":Esri_WorldTopoMap
    };

var overlayMaps = {
	"Prioritization":priorityLayer,
    "Score Change":differenceLayer
	};

L.control.layers(baseMaps,overlayMaps).addTo(map);

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
        '<i style="background:' + priorityColorScale (grades[i]) + '"></i> ' + '<h6 class="legendText">' + labels[i] + '</h6>' + '<br>';
}
    return div;
};

legend.addTo(map);
// Download Button

var download = L.control({position: 'bottomleft'});

download.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'button')
 	div.innerHTML = "<a href= "+serviceURL+ " download>"+ "<h6 class='download' >DOWNLOAD</h6></a>"


    return div;
};

download.addTo(map);


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
$(".slider").on("input",recomputeWeightedSum); // On Change