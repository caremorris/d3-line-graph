// Set up chart
var margin = {top: 20, right: 20, bottom: 30, left: 60},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// Scales          
var x = d3.time.scale()
    .range([0, width]);
            
var y = d3.scale.linear()
    .range([height, 0]);

// Axes         
var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
            
var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");
            
var line = d3.svg.line()    // returns a path generator; is both an object & a fxn
    .interpolate("basis")
    .x(function(d) { return x(d.time); }) // x is a function. it maps d.time to a pixel value between (0, width)
    .y(function(d) { return y(d.value); }); // y is a function. it maps d.value to a pixel value between (0, height) :)
            
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

d3.json("data/cincyWeather1990.json", function(error, data) {
    data.forEach(function(d) {
        d.time = +d.time;
        d.time *= 1000;
        d.value = +d.value;
    });

    // set the input domain. min and max.
    x.domain(d3.extent(data, function(d) { return d.time; }));
    y.domain(d3.extent(data, function(d) { return d.value; }));

    // x axis 
    svg.append("g")         
        .attr("class", "x axis")
        .attr("transform", "translate(0, " + height + ")")
        .call(xAxis);  

    // y axis   
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Temperature (Fahrenheit)");
    
    // line
    svg.append("path")
        .data(data) 
        .attr("class", "line") 
        .attr("d", line(data));
});


function update(data) {   
    data.forEach(function(d) {
        d.time = +d.time;
        d.time *= 1000;
        d.value = + d.value;
    });

    x.domain(d3.extent(data, function(d) { return d.time; }));
    y.domain(d3.extent(data, function(d) { return d.value; }));

    var svg = d3.select("body").transition();

    svg.select(".line")
        .duration(1000)
        .attr("d", line(data))
    svg.select(".x.axis")
        .duration(750)
        .call(xAxis)
    svg.select(".y.axis")
        .duration(750)
        .call(yAxis);
}

function load(name) {
    d3.json("data/"+name+".json", function(error, json) {
        update(json);
    });
}
