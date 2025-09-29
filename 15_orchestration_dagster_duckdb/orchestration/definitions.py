# ==================== #
#                      #
#       imports        #
#                      #
# ==================== #

import dlt
import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject

# to import dlt script
import sys
sys.path.insert(0, '../data_extract_load')
from load_job_ads import jobads_source 

# data warehouse directory
db_path = str(Path(__file__).parents[1] / "data_warehouse/job_ads.duckdb")

# ==================== #
#                      #
#       dlt Asset      #
#                      #
# ==================== #

# create dlt resource
dlt_resource = DagsterDltResource()

# create dlt asset
@dlt_assets(
    dlt_source = jobads_source(),
    dlt_pipeline = dlt.pipeline(
        pipeline_name="jobsearch",
        dataset_name="staging",
        destination=dlt.destinations.duckdb(db_path),
    ),
)
def dlt_load(context: dg.AssetExecutionContext, dlt: DagsterDltResource): 
    yield from dlt.run(context=context)

# ==================== #
#                      #
#       dbt Asset      #
#                      #
# ==================== #

# ==================== #
#                      #
#         Job          #
#                      #
# ==================== #

# ==================== #
#                      #
#       Schedule       #
#                      #
# ==================== #

# ==================== #
#                      #
#        Sensor        #
#                      #
# ==================== #

# ==================== #
#                      #
#     Definitions      #
#                      #
# ==================== #
