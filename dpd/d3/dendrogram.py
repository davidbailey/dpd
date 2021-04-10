import json
from string import Template


def dendrogram(d):
    """
    Template generator for creating a D3 dendrogram
    """
    template = Template(
        """
    <script src="https://d3js.org/d3.v4.js"></script>
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
    </script>
    """
    )
    svg = r"""
    <script>
    var svg = document.getElementById("svg");
    var serializer = new XMLSerializer();
    var source = serializer.serializeToString(svg);
    if(!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)){
        source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
    }
    if(!source.match(/^<svg[^>]+"http\:\/\/www\.w3\.org\/1999\/xlink"/)){
        source = source.replace(/^<svg/, '<svg xmlns:xlink="http://www.w3.org/1999/xlink"');
    }
    source = '<?xml version="1.0" standalone="no"?>' + source;
    var url = "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(source);
    document.getElementById("link").href = url;
    </script>
    """
    return template.substitute({"d": json.dumps(d)}) + svg
