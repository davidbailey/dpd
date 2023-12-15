from flask import Blueprint, Flask, Response, request

index = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <style>
            .mapid {
                height: 1024px;
                width: 768px;
            }
        </style>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A==" crossorigin="" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js" integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA==" crossorigin=""></script>
        <title>Agent-based Transportation Model</title>
    </head>
    <body>
        <div id="mapid" class="mapid"></div>
        <script type="text/javascript">
            var mymap = L.map("mapid").setView([38, -77], 9);
            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                attribution: 'Data by \u0026copy; \u003ca href=\"http://openstreetmap.org\"\u003eOpenStreetMap\u003c/a\u003e, under \u003ca href=\"http://www.openstreetmap.org/copyright\"\u003eODbL\u003c/a\u003e.',
                maxZoom: 18,
            }).addTo(mymap);
            var people;
            fetch("http://localhost:9000/people")
                .then(function (response) {
                    return response.json();
                })
                .then(function (json) {
                    people = L.geoJSON(json);
                    people.addTo(mymap);
                });
            var refreshPeople = function () {
                fetch("http://localhost:9000/people")
                    .then(function (response) {
                        return response.json();
                    })
                    .then(function (json) {
                        mymap.removeLayer(people);
                        people = L.geoJSON(json);
                        people.addTo(mymap);
                    });
            };
            setInterval(refreshPeople, 500);
        </script>
    </body>
</html>
"""

people = """
{"type": "FeatureCollection", "features": [] }
"""

root_blueprint = Blueprint("root", __name__)


@root_blueprint.route("/")
def root():
    return index


get_post_people_blueprint = Blueprint("get_post_people", __name__)


@get_post_people_blueprint.route("/people", methods=["GET", "POST"])
def get_post_people():
    global people
    if request.method == "POST":
        people = request.form["people"]
        return Response()
    else:
        resp = Response(people)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp


def people_flask_app():
    app = Flask(__name__)
    app.register_blueprint(root_blueprint)
    app.register_blueprint(get_post_people_blueprint)
    return app
