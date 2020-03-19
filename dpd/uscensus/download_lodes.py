from dpd.utils import download_file


def download_lodes_od(st, part, type_, year):
    """
    Download LODES OD file. APIS documentation from here: https://lehd.ces.census.gov/data/lodes/LODES7/LODESTechDoc7.4.pdf

    Args:
        st (str): lowercase, 2-letter postal code for a chosen state 
            e.g. "ca"
        part (str): Part of the state file, can have a value of either “main” or “aux”. Complimentary parts of the state file, the main part includes jobs with both workplace and residence in the state and the aux part includes jobs with the workplace in the state and the residence outside of the state.
            e.g. "main"
        type_ (str): Job Type, can have a value of “JT00” for All Jobs, “JT01” for Primary Jobs, “JT02” for All Private Jobs, “JT03” for Private Primary Jobs, “JT04” for All Federal Jobs, or “JT05” for Federal Primary Jobs.
            e.g. "JT00"
        year (str): Year of job data. Can have the value of 2002-2015 for most states.
            e.g. "2017"

    Returns:
        str: the local filename of the downloaded file
    """
    url = (
        "https://lehd.ces.census.gov/data/lodes/LODES7/%s/od/%s_od_%s_%s_%s.csv.gz"
        % (st, st, part, type_, year)
    )
    return download_file(url)


def download_lodes_xwalk(st):
    """
    Download LODES Crosswalk file. APIS documentation from here: https://lehd.ces.census.gov/data/lodes/LODES7/LODESTechDoc7.4.pdf

    Args:
        st (str): lowercase, 2-letter postal code for a chosen state 
            e.g. "ca"
            
    Returns:
        str: the local filename of the downloaded file
    """
    url = "https://lehd.ces.census.gov/data/lodes/LODES7/%s/%s_xwalk.csv.gz" % (st, st)
    return download_file(url)
