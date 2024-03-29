import logging
import os

import requests


def download_file(url, redownload=False, timeout=600):
    """
    Download a file locally. Does not download the file if it already exists.

    Args:
        url (str): the url of the file to download
        redownload (bool): if the file exists, delete it and redownload it

    Returns:
        local_filename (str): the local filename of the downloaded or existing file
    """
    local_filename = url.split("/")[-1]
    if redownload or not os.path.isfile(local_filename):
        logging.info("Downloading %s..." % (local_filename))
        with requests.get(url, stream=True, timeout=timeout) as r:
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        logging.info("Finished downloading %s" % (local_filename))
    return local_filename
