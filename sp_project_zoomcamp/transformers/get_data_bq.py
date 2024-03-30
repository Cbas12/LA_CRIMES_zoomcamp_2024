from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.bigquery import BigQuery
from os import path
from pandas import DataFrame
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform_in_bigquery(*args, **kwargs) -> DataFrame:
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    gcp_project = "spatial-vision-412003"

    query = (
        "CREATE OR REPLACE EXTERNAL TABLE `"+gcp_project+".sp_project_bq.external_crime_temp` "
        "OPTIONS ( format = 'parquet', uris = ['gs://sp_project_bucket/new_crime_data.parquet']);"
    )

    query_select = (
        "SELECT * FROM `"+gcp_project+".sp_project_bq.external_crime_temp`"
    )

    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).execute(query)


    return BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query_select)



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
