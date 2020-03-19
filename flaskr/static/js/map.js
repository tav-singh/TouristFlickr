
$(() => {
    // console.log($('#result').data().result)
    // let result = $('#result').data().result
    // console.log( (result) )
    // console.log( $('#result').data().pref )

    let tags = $('#result').data().pref.split(",")
    // console.log(tags)

    $('.tags').each(function(i, obj) {
        for (tag of tags) {
            if ($(this)[0].id === "t-"+ tag)
                $(this).removeClass('tagDisabled')
        }
    });
})

//change tag
$(".tags").on('click', (event) => {
    let newTag = event.currentTarget.id.replace("t-", "")
    if (newTag !== $('#result').data().pref) {
        location.href = Flask.url_for('user_pref', {pref: newTag});
    }
})

$("#close-city").click(() => {
    console.log("click")
        d3.select("#one-city-views").style("display", "none")
        cityOpened = false

}) 


var tags = $('#result').data().pref.split(",")
tagColors = {
    city: "fbc11a",
    nature: "5f6c11",
    beach: "262244",
    architecture: "ec7ead",
    lake: "fade98",
    mountains: "463a3a"
}
var donutColour = ["#fade98", "#5f6c11", "#fbc11a", "#ec7ead", "#274b69", "#463a3a"];
// DEFINE VARIABLES #463a3a
// Define size of map group
// Full world map is 2:1 ratio
// Using 12:5 because we will crop top and bottom of map
w = 3000;
h = 1250;
// variables for catching min and max zoom factors
var minZoom;
var maxZoom;

// DEFINE FUNCTIONS/OBJECTS
// Define map projection
var projection = d3
    .geoEquirectangular()
    .center([0, 15]) // set centre to further North as we are cropping more off bottom of map
    .scale([w / (2 * Math.PI)]) // scale to fit group width
    .translate([w / 2, h / 2]) // ensure centred in group
;

// Define map path
var path = d3
    .geoPath()
    .projection(projection);

// Create function to apply zoom to countriesGroup
function zoomed() {
    t = d3
        .event
        .transform;
    countriesGroup
        .attr("transform", "translate(" + [t.x, t.y] + ")scale(" + t.k + ")");
}   

// Define map zoom behaviour
var zoom = d3
    .zoom()
    .on("zoom", zoomed);

function getTextBox(selection) {
    selection
        .each(function (d) {
            d.bbox = this
                .getBBox();
        });
}

// Function that calculates zoom/pan limits and sets zoom to default value 
function initiateZoom() {
    // Define a "minzoom" whereby the "Countries" is as small possible without leaving white space at top/bottom or sides
    minZoom = Math.max($("#map-holder").width() / w, $("#map-holder").height() / h);
    // set max zoom to a suitable factor of this value
    maxZoom = 20 * minZoom;
    // set extent of zoom to chosen values
    // set translate extent so that panning can't cause map to move out of viewport
    zoom
        .scaleExtent([minZoom, maxZoom])
        .translateExtent([
            [0, 0],
            [w, h]
        ]);
    // define X and Y offset for centre of map to be shown in centre of holder
    midX = ($("#map-holder").width() - minZoom * w) / 2;
    midY = ($("#map-holder").height() - minZoom * h) / 2;
    // change zoom transform to min zoom and centre offsets
    svg.call(zoom.transform, d3.zoomIdentity.translate(midX, midY).scale(minZoom));
}

// zoom to show a bounding box, with optional additional padding as percentage of box size
function boxZoom(box, centroid, paddingPerc) {
    minXY = box[0];
    maxXY = box[1];
    // find size of map area defined
    zoomWidth = Math.abs(minXY[0] - maxXY[0]);
    zoomHeight = Math.abs(minXY[1] - maxXY[1]);
    // find midpoint of map area defined
    zoomMidX = centroid[0];
    zoomMidY = centroid[1];
    // increase map area to include padding
    zoomWidth = zoomWidth * (1 + paddingPerc / 100);
    zoomHeight = zoomHeight * (1 + paddingPerc / 100);
    // find scale required for area to fill svg
    maxXscale = $("svg").width() / zoomWidth;
    maxYscale = $("svg").height() / zoomHeight;
    zoomScale = Math.min(maxXscale, maxYscale);
    // handle some edge cases
    // limit to max zoom (handles tiny countries)
    zoomScale = Math.min(zoomScale, maxZoom);
    // limit to min zoom (handles large countries and countries that span the date line)
    zoomScale = Math.max(zoomScale, minZoom);
    // Find screen pixel equivalent once scaled
    offsetX = zoomScale * zoomMidX;
    offsetY = zoomScale * zoomMidY;
    // Find offset to centre, making sure no gap at left or top of holder
    dleft = Math.min(0, $("svg").width() / 2 - offsetX);
    dtop = Math.min(0, $("svg").height() / 2 - offsetY);
    // Make sure no gap at bottom or right of holder
    dleft = Math.max($("svg").width() - w * zoomScale, dleft);
    dtop = Math.max($("svg").height() - h * zoomScale, dtop);
    // set zoom
    svg
        .transition()
        .duration(500)
        .call(
            zoom.transform,
            d3.zoomIdentity.translate(dleft, dtop).scale(zoomScale)
        );
}

// on window resize
$(window).resize(function () {
    // Resize SVG
    svg
        .attr("width", $("#map-holder").width())
        .attr("height", $("#map-holder").height());
    initiateZoom();
});

// create an SVG
var svg = d3
    .select("#map-holder")
    .append("svg")
    // set to the same size as the "map-holder" div
    .attr("width", $("#map-holder").width())
    .attr("height", $("#map-holder").height())
    .style("fill",  "rgb(147,200,230)")
    .classed("svg-content-responsive", true)
    // add zoom functionality
    .call(zoom);



// var result = '{{ result }}'
// document.getElementById('print').innerHTML = result[0].longitude+','+result[0].latitude;
// Create data for donut:
var data = $('#result').data().result;
console.log(data)
var continentColour = {
"Asia": "#fd9644",
"Europe": "#a55eea",
"North America": "#fc5c65",
"South America": "#26de81",
"Africa": "#778ca3",
"Australia": "#d1d8e0"
}

// get map data
d3.json(
    "../static/json/custom50.json",
    function (json) {
        //Bind data and create one path per GeoJSON feature
        countriesGroup = svg.append("g").attr("id", "map");
        // add a background rectangle
        countriesGroup
            .append("rect")
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", w)
            .attr("height", h);

        // draw a path for each feature/country
        countries = countriesGroup
            .selectAll("path")
            .data(json.features)
            .enter()
            .append("path")
            .attr("d", path)
            .attr("id", function (d, i) {
                return "country" + d.properties.iso_a3;
            })
            //.style("fill", function (d) {
            //    console.log(d.properties);
            //    return continentColour[d.properties.continent];
            //})
            .attr("class", "country")
            // .attr("stroke-width", 1)
            // .attr("stroke", "#ff0000")


            // add a mouseover action to show name label for feature/country
            .on("mouseover", function (d, i) {
                d3.select("#countryLabel" + d.properties.iso_a3).style("display", "block");
            })
            .on("mouseout", function (d, i) {
                d3.select("#countryLabel" + d.properties.iso_a3).style("display", "none");
            })
            // add an onclick action to zoom into clicked country
            .on("click", function (d, i) {
                d3.selectAll(".country").classed("country-on", false);
                d3.select(this).classed("country-on", true);
                boxZoom(path.bounds(d), path.centroid(d), 20);
            });
                

            // set the dimensions and margins of the graph
        var width = 40
            height = 40
            margin = 3

        // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
        var radius = Math.min(width, height) / 2 - margin

        for ( idx in data) {

            // set the color scale
            // console.log(data[idx])
            let clso = data[idx].class_tag_overall
            var data_pie = {city: 0, nature: 0, beach: 0, architecture: 0, lake: 0, mountains: 0}
            for (tag of tags) {
                if(clso[tag]) data_pie[tag] = clso[tag]
            }

            var color = d3.scaleOrdinal()
            .domain(data_pie)
            .range(donutColour)
            // console.log(donutColour);
            // Compute the position of each group on the pie:
            var pie = d3.pie()
            .value(function(d) {return d.value; })
            var data_ready = pie(d3.entries(data_pie))

            let de = data[idx]    

            var donut = countriesGroup
            .selectAll('donuts')
            .data(data_ready)
            .enter()
            .append('path')
            .attr('d', d3.arc()
            .innerRadius(7)         // This is the size of the donut hole
            .outerRadius(radius)
            )
            .attr("transform", function(d) {return "translate(" + projection([de.longitude, de.latitude])[0] +"," + projection([de.longitude, de.latitude])[1] + ")" })
            // .attr("cx", function(d){ return projection([4, 52])[0] })
            // .attr("cy", function(d){ return projection([4, 52])[1] })
            .attr('fill', function(d){
                // console.log(d)
                return(color(d.data.key))
            })
            .attr("stroke", "black")
            .style("stroke-width", "0px")
            .on("click", () => getCityInfo(de))
            .on("mouseover", function (d, i) {
                d3.select(this).style("cursor", "pointer"); 
            })
            .on("mouseout", function (d, i) {
                d3.select(this).style("cursor", "default"); 
            })

            // let group = countriesGroup
            //             .append("g")
            //             .attr("transform", function(d) {return "translate(" + projection([de.longitude, de.latitude])[0] +"," + projection([de.longitude, de.latitude])[1] + ")" })

            var defs = countriesGroup.append('svg:defs')

            defs.append("svg:pattern")
                .attr("id", "img-pop" + idx)
                .attr("width", "100%") 
                .attr("height", "100%")
                .attr("patternUnits", "userSpaceOnUse")
                .append("svg:image")
                .attr("xlink:href", de.description[0].cdn_url)
                .attr("width", 50)
                .attr("height", 50)
                .attr("x", 0)
                .attr("y", 0)
                
                var rectImage = countriesGroup.append("rect")
                .attr("transform", function(d) {return "translate(" + projection([de.longitude - 3, de.latitude + 8])[0] +"," + projection([de.longitude - 3, de.latitude + 8])[1] + ")" })
                .attr("width", 50)
                .attr("height", 50)
                // .attr("r", 100 / 2)
                .attr("class", "image-pop")
                // .style("fill", "#fff")
                .style("fill", "url(#img-pop" + idx + ")")
                .on("mouseover", function () {
                    d3.select(this).style("cursor", "pointer"); 
                    let pos = d3.select(this).node().getBoundingClientRect()
                    console.log(pos.left)
                    const vw = Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
                    const vh = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)

                    vwPosLeftOffset = pos.left < vw/2 ? 125 : (-275)
                    vhPosTopOffset = pos.top < vh /2 ? 0 : (-175)

                    $( "<div></div>", {
                        "id": "div-img-pop"
                    }).appendTo( "#main-cont" );
                    $("#div-img-pop").css({
                        display: "flex",
                        "flex-direction": "column-reverse",
                        position: "absolute",   
                        top: pos.top + vhPosTopOffset,
                        left: pos.left + vwPosLeftOffset,
                        background: "white",
                        height: "250px",
                        width: "250px",
                        "border-radius": "15px",
                        background: "url("+de.description[0].cdn_url + ")",
                        "background-size" : "cover",
                        "background-position" : "center"

                    })

                    $( "<div></div>", {
                        "id": "div-img-pop-layer"
                    }).appendTo( "#div-img-pop" );

                    $( "<p></p>", {
                        "id": "div-img-pop-p"
                    }).appendTo( "#div-img-pop" );

                    $("#div-img-pop-p").text(de.city + ", " + de.country)
                })
                .on("mouseout", function (d, i) {
                    d3.select(this).style("cursor", "default"); 
                    $("#div-img-pop").css("display", "none")
                    $("#div-img-pop").empty()

                })
                .on("click", () => getCityInfo(de))

            // countriesGroup
            // .append("svg:image")
            // .attr("xlink:href", de.description[0].cdn_url)
            // .attr("transform", function(d) {return "translate(" + projection([de.longitude, de.latitude])[0] +"," + projection([de.longitude, de.latitude])[1] + ")" })
            // .attr("class", "image-pop")
            // .attr("x", "200")
            //end of for point gen.
        }

        function getCityInfo(val) {
            console.log("sending...")
            console.log(val)
            // console.log(val)
            $.ajax({
            url: "/city_info",
            type: "get",
            data: {data: JSON.stringify(val)},
            success: function(response) {
                console.log("success")
                console.log(response)
                $("#one-city-views").html(response.results)
                openCityInfo()
            },
            error: function(xhr) {
                alert("Err city info load")
                console.log(xhr)
            }
            });
        }

        function openCityInfo() {
            $(".overlay").css("width", "800px")
            svg
            .attr("width", "100%")
            initiateZoom();
            // d3.select("#one-city-views").style("display", "block")
            cityOpened = true
        }
        
        // Add a label group to each feature/country. This will contain the country name and a background rectangle
        // Use CSS to have class "countryLabel" initially hidden
        countryLabels = countriesGroup
            .selectAll("g")
            .data(json.features)
            .enter()
            .append("g")
            .attr("class", "countryLabel")
            .attr("id", function (d) {
                return "countryLabel" + d.properties.iso_a3;
            })
            .attr("transform", function (d) {
                return (
                    "translate(" + path.centroid(d)[0] + "," + path.centroid(d)[1] + ")"
                );
            })
            // add mouseover functionality to the label
            .on("mouseover", function (d, i) {
                d3.select(this).style("display", "block");
            })
            .on("mouseout", function (d, i) {
                d3.select(this).style("display", "none");
            })
            // add an onlcick action to zoom into clicked country
            .on("click", function (d, i) {
                d3.selectAll(".country").classed("country-on", false);
                d3.select("#country" + d.properties.iso_a3).classed("country-on", true);
                boxZoom(path.bounds(d), path.centroid(d), 20);
            });
        // add the text to the label group showing country name
        countryLabels
            .append("text")
            .attr("class", "countryName")
            .style("text-anchor", "middle")
            .attr("dx", 0)
            .attr("dy", 0)
            .text(function (d) {
                return d.properties.name;
            })
            .call(getTextBox);
        // add a background rectangle the same size as the text
        countryLabels
            .insert("rect", "text")
            .attr("class", "countryLabelBg")
            .attr("transform", function (d) {
                return "translate(" + (d.bbox.x - 2) + "," + d.bbox.y + ")";
            })
            .attr("width", function (d) {
                return d.bbox.width + 4;
            })
            .attr("height", function (d) {
                return d.bbox.height;
            });
        initiateZoom();

    }
);