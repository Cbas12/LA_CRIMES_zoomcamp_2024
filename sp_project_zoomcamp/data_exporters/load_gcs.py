from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'sp_project_bucket'
    object_key = 'new_crime_data.parquet'

    get_date = df['Date Rptd'].str[6:10]+df['Date Rptd'].str[0:2]+df['Date Rptd'].str[3:5]
    date_val = str(get_date.min())+"_"+get_date.max()
    story_object_key = 'historical_data/'+date_val+".parquet"
    #print(story_object_key)

    #load to historic data
    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        story_object_key,
    )

    #load to temporal table
    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )