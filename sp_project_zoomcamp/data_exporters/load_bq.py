from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path
import pandas as pd


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

def load_to_bq(def_df,def_table_id,def_config_path,def_config_profile):
    BigQuery.with_config(ConfigFileLoader(def_config_path, def_config_profile)).export(
        def_df,
        def_table_id,
        #if_exists='replace'
        if_exists='append'
    )

@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:  
    
    #spatial-vision-412003.sp_project_bq.LA_CRIME_DATA
    table_id = 'spatial-vision-412003.sp_project_bq.LA_CRIME_DATA'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    #compare dates
    query_max_date = "SELECT MAX(DATE_REPORTED) FROM `spatial-vision-412003.sp_project_bq.LA_CRIME_DATA`;"
    bq_max_date = BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query_max_date)
    bq_max_date = str(bq_max_date.iloc[0,0])
    print("\\nbq_max_date: "+bq_max_date+"\\n")

    if ("NaT") in bq_max_date:
        df_filter_date = df
        print("All records are new data...")
    else:
        dt_bq_max_date = pd.Timestamp(bq_max_date).date()
        df_filter_date = df[df['DATE_REPORTED'] > dt_bq_max_date]
        print(str(df_filter_date.shape[0])+" rows are new data...")

    #load data to LA_CRIME_DATA
    total_rows = int(df_filter_date.shape[0])
    
    if total_rows != 0:
        load_to_bq(df_filter_date,table_id,config_path,config_profile)
        print("\\n"+str(total_rows)+" rows loaded...")
    else:
        print("\\nNo rows to load...")
    
