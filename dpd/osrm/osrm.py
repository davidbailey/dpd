import os.path
import subprocess

from dpd.utils import download_file


class OSRM:
    def __init__(
        self,
        region,
        profile,
        profile_directory="/usr/local/Cellar/osrm-backend/5.22.0_1/share/osrm/profiles/",
    ):
        url = "https://download.geofabrik.de/%s-latest.osm.pbf" % (region)
        self.filename = download_file(url)
        self.profile = profile
        self.profile_directory = profile_directory

    def extract(self, *args, **kwargs):
        print("Extracting " + self.filename)
        return subprocess.run(
            [
                "osrm-extract",
                "-p",
                self.profile_directory + self.profile + ".lua",
                self.filename,
            ],
            *args,
            **kwargs
        )

    def contract(self, *args, **kwargs):
        if not os.path.isfile(self.filename.split(".osm.pbf")[0] + ".osrm.hsgr"):
            self.contract()
        print("Contracting " + self.filename)
        return subprocess.run(["osrm-contract", self.filename], *args, **kwargs)

    def routed(self, *args, **kwargs):
        if not os.path.isfile(self.filename.split(".osm.pbf")[0] + ".osrm"):
            self.extract()
        return subprocess.Popen(["osrm-routed", self.filename], *args, **kwargs)
