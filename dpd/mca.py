import pandas
import numpy

class MultipleCriteriaAnalysis:
    def __init__(self, attributes, alternatives, monte_carlo=False):
        self.attributes = attributes
        self.alternatives = alternatives
        self.monte_carlo = monte_carlo
        if monte_carlo:
            monte_carlo = ['Mean', 'Standard Deviation', 'Distribution']
            index = pandas.MultiIndex.from_product([attributes, monte_carlo])
            self.mca = pandas.DataFrame(numpy.zeros((len(attributes) * len(monte_carlo), len(alternatives))),
                                        index=index, columns=alternatives, dtype='object')
        else:
            self.mca = pandas.DataFrame(numpy.zeros((len(attributes), len(alternatives))),
                                        index=attributes, columns=alternatives)
        self.weights = pandas.Series(numpy.ones(len(attributes)), index=attributes)

    def from_csvs(mca_file='mca.csv', weights_file='weights.csv', monte_carlo=False):
        mca = MultipleCriteriaAnalysis([], [])
        if monte_carlo == True:
            mca.mca = pandas.read_csv(mca_file, index_col=[0,1])
            mca.mca.index.names = [None] * len(mca.mca.index.names)
            mca.attributes = list(mca.mca.index[0])
            mca.monte_carlo = True
        else:
            mca.mca = pandas.DataFrame.from_csv(mca_file)
            mca.attributes = list(mca.mca.index)
            mca.monte_carlo = False
        mca.alternatives = list(mca.mca.columns)
        mca.weights = pandas.Series.from_csv(weights_file)
        return mca


    def to_csvs(self, mca_file='mca.csv', weights_file='weights.csv'):
        self.mca.to_csv(mca_file)
        self.weights.to_csv(weights_file)


    def to_d3(self):
        data = {"name": "Multiple Criteria Analysis", "children": []}
        for attribute in self.attributes:
            children = []
            for alternative in self.alternatives:
                if self.monte_carlo:
                    children.append({'name': alternative, 'mean': self.mca[alternative][attribute]['Mean'],
                                     'stddev': self.mca[alternative][attribute]['Standard Deviation'],
                                     'distribution': self.mca[alternative][attribute]['Distribution']})
                else:
                    children.append({'name': alternative, 'mean': self.mca[alternative][attribute]})
            data['children'].append({'name': attribute, 'weight': self.weights[attribute], 'alternatives': children})
        return data


    def radar_chart(self):
        legend_options = self.alternatives
        d = []
        for alternative in self.alternatives:
            alternative_d = []
            for attribute in self.attributes:
                alternative_d.append({'axis': attribute, 'value': self.mca[alternative][attribute]})
            d.append(alternative_d)

        template = Template('''
        <script src="https://d3js.org/d3.v3.min.js"></script>
        <script src="https://raw.githubusercontent.com/davidbailey/dpd/master/js/RadarChart.js"></script>
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
HTML(template.substitute({'legend_options': json.dumps(legend_options), 'd': json.dumps(d), 'title': 'Alternative'}))
