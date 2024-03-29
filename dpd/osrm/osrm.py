import logging
import os.path
import subprocess  # nosec

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
        logging.info("Extracting " + self.filename)
        return subprocess.run(  # nosec
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
        if not os.path.isfile(self.filename.split(".osm.pbf")[0] + ".osrm"):
            self.extract()
        logging.info("Contracting " + self.filename)
        return subprocess.run(  # nosec
            ["osrm-contract", self.filename], *args, **kwargs
        )

    def routed(self, *args, **kwargs):
        if not os.path.isfile(self.filename.split(".osm.pbf")[0] + ".osrm.hsgr"):
            self.contract()
        return subprocess.Popen(  # nosec
            ["osrm-routed", self.filename], *args, **kwargs
        )
