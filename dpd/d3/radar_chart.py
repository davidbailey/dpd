import json
from string import Template


def radar_chart(legend_options, d, title):
    """
    Template generator for creating a D3 radar chart
    """
    template = Template(
        """
    <script src="https://d3js.org/d3.v3.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/davidbailey/dpd@master/js/RadarChart.js"></script>
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
    """
    )
    return template.substitute(
        {
            "legend_options": json.dumps(legend_options),
            "d": json.dumps(d),
            "title": title,
        }
    )
