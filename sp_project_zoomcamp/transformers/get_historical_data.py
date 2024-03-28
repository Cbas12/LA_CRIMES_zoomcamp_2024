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

    query_select = (
        "SELECT * FROM `spatial-vision-412003.sp_project_bq.external_crime_temp_full`"
        "WHERE Date_Rptd LIKE '%/2023%' AND LEFT(Date_Rptd,2) IN ('07','08','09','10','11','12');"
    )
    #"WHERE Date_Rptd LIKE '%/2023%' AND LEFT(Date_Rptd,2) IN ('01','02','03','04','05','06');"
    #"WHERE Date_Rptd LIKE '%/2023%' AND LEFT(Date_Rptd,2) IN ('07','08','09','10','11','12');"

    #BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).execute(query)


    return BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query_select)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
