from dpd.utils import download_file


def download_lodes_data(data, st, part_or_seg, type_, year):
    """
    Download LODES OD file. APIS documentation from here: https://lehd.ces.census.gov/data/lodes/LODES7/LODESTechDoc7.4.pdf

    Args:
        data (str): one of "od", "rac", or "wac"
            e.g. "od"
        st (str): lowercase, 2-letter postal code for a chosen state
            e.g. "ca"
        part_or_seg (str): If data is od, part of the state file, can have a value of either “main” or “aux”. Complimentary parts of the state file, the main part includes jobs with both workplace and residence in the state and the aux part includes jobs with the workplace in the state and the residence outside of the state. If data is rac or wac, segment of the workforce, can have the values of “S000”, “SA01”, “SA02”, “SA03”, “SE01”, “SE02”, “SE03”, “SI01”, “SI02”, or “SI03”. These correspond to the same segments of the workforce as are listed in the OD file structure.
            e.g. "main"
        type_ (str): Job Type, can have a value of “JT00” for All Jobs, “JT01” for Primary Jobs, “JT02” for All Private Jobs, “JT03” for Private Primary Jobs, “JT04” for All Federal Jobs, or “JT05” for Federal Primary Jobs.
            e.g. "JT00"
        year (str): Year of job data. Can have the value of 2002-2015 for most states.
            e.g. "2017"

    Returns:
        str: the local filename of the downloaded file
    """
    data_values = ["od", "rac", "wac"]
    if data not in data_values:
        raise ValueError("data must be one of " + str(data_values))
    if data == "od":
        part_values = ["main", "aux"]
        if part_or_seg not in part_values:
            raise ValueError(
                "part_or_seg must be one of "
                + str(part_values)
                + "when data is "
                + data
            )
    elif data in ["rac", "wac"]:
        seg_values = [
            "S000",
            "SA01",
            "SA02",
            "SA03",
            "SE01",
            "SE02",
            "SE03",
            "SI01",
            "SI02",
            "SI03",
        ]
        if part_or_seg not in seg_values:
            raise ValueError(
                "part_or_seg must be one of " + str(seg_values) + "when data is " + data
            )
    type_values = ["JT00", "JT01", "JT02", "JT03", "JT04", "JT05"]
    if type_ not in type_values:
        raise ValueError("type_ must be one of " + str(type_values))
    url = (
        "https://lehd.ces.census.gov/data/lodes/LODES7/%s/%s/%s_%s_%s_%s_%s.csv.gz"
        % (st, data, st, data, part_or_seg, type_, year)
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
