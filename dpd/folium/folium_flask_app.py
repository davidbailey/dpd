import folium
from flask import Blueprint, Flask, Response, session
from jinja2 import Template


class ClickForMarkerWithCallback(folium.ClickForMarker):
    _template = Template(
        """
            {% macro script(this, kwargs) %}
                function newMarker(e){
                    var new_mark = L.marker().setLatLng(e.latlng).addTo({{this._parent.get_name()}});
                    new_mark.dragging.enable();
                    new_mark.on('dblclick', function(e){
                        {{this._parent.get_name()}}.removeLayer(e.target)
                        httpRequest = new XMLHttpRequest();
                        httpRequest.onreadystatechange = load_results
                        httpRequest.open('GET', 'http://localhost:9000/remove_point/lat/' + e.latlng.lat.toFixed(4) + '/lng/' + e.latlng.lng.toFixed(4));
                        httpRequest.send();
                    })
                    var lat = e.latlng.lat.toFixed(4),
                       lng = e.latlng.lng.toFixed(4);
                    new_mark.bindPopup({{ this.popup }});
                    httpRequest = new XMLHttpRequest();
                    httpRequest.onreadystatechange = load_results
                    httpRequest.open('GET', 'http://localhost:9000/add_point/lat/' + lat + '/lng/' + lng);
                    httpRequest.send();
                    };
                      function load_results() {
                        if (httpRequest.readyState === XMLHttpRequest.DONE) {
                            document.getElementById('results').innerHTML = httpRequest.responseText;
                        }
                      }
                {{this._parent.get_name()}}.on('click', newMarker);
            {% endmacro %}
            """
    )

    def __init__(self, popup=None):
        super(ClickForMarkerWithCallback, self).__init__()


root_blueprint = Blueprint("root", __name__)


@root_blueprint.route("/")
def root():
    session["points"] = []
    m = folium.Map(location=[34.05, -118.25])
    m.add_child(ClickForMarkerWithCallback())
    resp = Response(m.get_root().render() + '<div id="results"></div>')
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


add_point_blueprint = Blueprint("add_point", __name__)


@add_point_blueprint.route("/add_point/lat/<lat>/lng/<lng>")
def add_point(lat, lng):
    points = session["points"]
    points.append((float(lng), float(lat)))
    session["points"] = points
    resp = Response(str(session["points"]))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


remove_point_blueprint = Blueprint("remove_point", __name__)


@remove_point_blueprint.route("/remove_point/lat/<lat>/lng/<lng>")
def remove_point(lat, lng):
    points = session["points"]
    points.remove((float(lng), float(lat)))
    session["points"] = points
    resp = Response(str(session["points"]))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


def folium_flask_app():
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.register_blueprint(add_point_blueprint)
    app.register_blueprint(remove_point_blueprint)
    app.register_blueprint(root_blueprint)
    return app
