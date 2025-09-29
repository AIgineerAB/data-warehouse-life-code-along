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

# data warehouse directory
db_path = str(Path(__file__).parents[1] / "data_warehouse/job_ads.duckdb")

def _get_ads(url_for_search, params):
    headers = {"accept": "application/json"}
    response = requests.get(url_for_search, headers=headers, params=params)
    response.raise_for_status()  
    return json.loads(response.content.decode("utf8"))


@dlt.resource(write_disposition="replace")
def jobads_resource(params):

    url = "https://jobsearch.api.jobtechdev.se"
    url_for_search = f"{url}/search"

    for ad in _get_ads(url_for_search, params)["hits"]:
        yield ad


def run_pipeline(table_name):
    pipeline = dlt.pipeline(
        pipeline_name="jobsearch",
        destination=dlt.destinations.duckdb(db_path), #update destination
        dataset_name="staging",
    )

    params = {"limit": 100, "occupation-field": "6Hq3_tKo_V57"}

    load_info = pipeline.run(jobads_resource(params=params), table_name=table_name)
    print(load_info)


if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    run_pipeline(table_name="technical_field_job_ads")
