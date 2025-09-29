#========================================#
#                                        #
#    This script loads job ads for       #
#    "Yrken med teknisk inriktning"      #
#                                        #
#========================================#


import dlt
import requests
import json
from pathlib import Path
import os

params = {"limit": 100, "occupation-field": "6Hq3_tKo_V57"}


def _get_ads(url_for_search, params):
    headers = {"accept": "application/json"}
    response = requests.get(url_for_search, headers=headers, params=params)
    response.raise_for_status()  
    return json.loads(response.content.decode("utf8"))


@dlt.resource(table_name = "technical_field_job_ads",
              write_disposition="replace")
def jobads_resource(params):

    url = "https://jobsearch.api.jobtechdev.se"
    url_for_search = f"{url}/search"

    for ad in _get_ads(url_for_search, params)["hits"]:
        yield ad


@dlt.source
def jobads_source():
    return jobads_resource(params)

