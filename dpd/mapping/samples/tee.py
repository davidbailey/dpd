from networkx import DiGraph
from shapely.geometry import LineString, Point

graph = DiGraph()

zero = Point(0, 0)
one = Point(100, 0)
two = Point(300, 0)
three = Point(600, 0)
four = Point(100, 400)

graph.add_nodes_from(
    [
        (0, {"geometry": zero}),
        (1, {"geometry": one, "type": "stop", "dwell_time": 10}),
        (2, {"geometry": two}),
        (3, {"geometry": three}),
        (4, {"geometry": four}),
    ]
)

zero_one = LineString([zero, one])
one_two = LineString([one, two])
two_three = LineString([two, three])
one_four = LineString([one, four])
one_zero = LineString([one, zero])
two_one = LineString([two, one])
three_two = LineString([three, two])
four_one = LineString([four, one])

graph.add_edges_from(
    [
        (
            0,
            1,
            {
                "geometry": zero_one,
                "length": zero_one.length,
                "lanes": 1,
                "maxspeed": 10,
            },
        ),
        (
            1,
            2,
            {"geometry": one_two, "length": one_two.length, "lanes": 1, "maxspeed": 10},
        ),
        (
            2,
            3,
            {
                "geometry": two_three,
                "length": two_three.length,
                "lanes": 1,
                "maxspeed": 10,
            },
        ),
        (
            1,
            4,
            {
                "geometry": one_four,
                "length": one_four.length,
                "lanes": 2,
                "maxspeed": 20,
            },
        ),
        (
            1,
            0,
            {
                "geometry": one_zero,
                "length": one_zero.length,
                "lanes": 1,
                "maxspeed": 10,
            },
        ),
        (
            2,
            1,
            {"geometry": two_one, "length": two_one.length, "lanes": 1, "maxspeed": 10},
        ),
        (
            3,
            2,
            {
                "geometry": three_two,
                "length": three_two.length,
                "lanes": 1,
                "maxspeed": 10,
            },
        ),
        (
            4,
            1,
            {
                "geometry": four_one,
                "length": four_one.length,
                "lanes": 2,
                "maxspeed": 20,
            },
        ),
    ]
)
