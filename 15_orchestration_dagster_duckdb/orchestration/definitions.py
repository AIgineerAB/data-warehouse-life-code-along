# ==================== #
#                      #
#       imports        #
#                      #
# ==================== #

from pathlib import Path
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

# related paths for dbt project
dbt_project_directory = Path(__file__).parents[1] / "data_transformation"
profiles_dir = Path.home() / ".dbt"

# create dagster dbt project object
dbt_project = DbtProject(project_dir=dbt_project_directory,
                         profiles_dir=profiles_dir)

dbt_resource = DbtCliResource(project_dir=dbt_project)

# create a manifest json file 
dbt_project.prepare_if_dev()

# create dagster dbt asset
@dbt_assets(manifest=dbt_project.manifest_path)

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

defs = dg.Definitions(assets=[dlt_load],
                      resources={"dlt": dlt_resource},
                      )