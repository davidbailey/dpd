import json
from string import Template

def radar_chart(legend_options, d, title):
    template = Template('''
    <script src="https://d3js.org/d3.v4.min.js"></script>
    <script src="https://cdn.rawgit.com/davidbailey/dpd/master/js/RadarChart.js"></script>
    <div id="body">
        <div id="chart"></div>
    </div>
    <script>
        var w = 500, h = 500;
        var colorscale = d3.scale.category10();
        var LegendOptions = $legend_options;
        var d = $d;

        RadarChart.draw("#chart", d);

        var svg = d3.select('#body')
            .selectAll('svg')
            .append('svg')
            .attr("width", w+300)
            .attr("height", h)
        var text = svg.append("text")
            .attr("class", "title")
            .attr('transform', 'translate(90,0)')
            .attr("x", w - 70)
            .attr("y", 10)
            .attr("font-size", "12px")
            .attr("fill", "#404040")
            .text("$title");
        var legend = svg.append("g")
            .attr("class", "legend")
            .attr("height", 100)
            .attr("width", 200)
            .attr('transform', 'translate(90,20)');
        legend.selectAll('rect')
            .data(LegendOptions)
            .enter()
            .append("rect")
            .attr("x", w - 65)
            .attr("y", function(d, i){ return i * 20;})
            .attr("width", 10)
            .attr("height", 10)
            .style("fill", function(d, i){ return colorscale(i);});
        legend.selectAll('text')
            .data(LegendOptions)
            .enter()
            .append("text")
            .attr("x", w - 52)
            .attr("y", function(d, i){ return i * 20 + 9;})
            .attr("font-size", "11px")
            .attr("fill", "#737373")
            .text(function(d) { return d; });
    </script>
    ''')
    return template.substitute({'legend_options': json.dumps(legend_options), 'd': json.dumps(d), 'title': title})

def dendrogram(d):
    template = Template('''
<svg id="svg" width="1400" height="1000">
  <style>

  .node circle {
    fill: #999;
  }

  .node text {
    font: 10px sans-serif;
  }

  .node--internal circle {
    fill: #555;
  }

  .node--internal text {
    text-shadow: 0 1px 0 #fff, 0 -1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff;
  }

  .link {
    fill: none;
    stroke: #555;
    stroke-opacity: 0.4;
    stroke-width: 1.5px;
  }

  </style>
</svg>
<a id="link">download .svg</a>
<script src="https://d3js.org/d3.v4.min.js"></script>
<script>
var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    g = svg.append("g").attr("transform", "translate(440,0)");

var tree = d3.cluster()
    .size([height, width - 800]);

var root = d3.hierarchy($d);

tree(root);

var link = g.selectAll(".link")
    .data(root.descendants().slice(1))
  .enter().append("path")
    .attr("class", "link")
    .attr("d", function(d) {
      return "M" + d.y + "," + d.x
          + "C" + (d.parent.y + 100) + "," + d.x
          + " " + (d.parent.y + 100) + "," + d.parent.x
          + " " + d.parent.y + "," + d.parent.x;
    });

var node = g.selectAll(".node")
    .data(root.descendants())
  .enter().append("g")
    .attr("class", function(d) { return "node" + (d.children ? " node--internal" : " node--leaf"); })
    .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

node.append("circle")
    .attr("r", 5);

node.append("text")
    .attr("dy", 8)
    .attr("x", function(d) { return d.children ? -8 : 8; })
    .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
    .style("font-size", "18px")
    .text(function(d) { return d.data.name});


var svg = document.getElementById("svg");
var serializer = new XMLSerializer();
var source = serializer.serializeToString(svg);
var url = "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(source);
document.getElementById("link").href = url;
</script>
    ''')
    return template.substitute({'d': json.dumps(d)})
