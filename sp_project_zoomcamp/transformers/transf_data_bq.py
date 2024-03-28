from pyspark.sql import types
from pyspark.sql import functions as F
import pyspark.pandas as ps
import numpy as np

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    spark = kwargs.get('spark')

    df = spark.createDataFrame(data)

    #modify df
    df =  df.withColumn("Date_Rptd", F.to_date(df["Date_Rptd"], "MM/dd/yyyy hh:mm:ss a")) \
            .withColumn("DATE_OCC", F.to_date(df["DATE_OCC"], "MM/dd/yyyy hh:mm:ss a")) \
            .withColumn("Vict_Age", F.when(F.col('Vict_Age') == 0, None).otherwise(F.col('Vict_Age'))) \
            .withColumn('Vict_Sex', F.when(~F.col('Vict_Sex').isin(['M', 'F']), 'Other')
                                        .otherwise(F.when(F.col('Vict_Sex') == 'M', 'Male')
                                        .otherwise(F.when(F.col('Vict_Sex') == 'F', 'Female'))) ) \
            .withColumn('TIME_OCC', F.when(F.length(F.col('TIME_OCC')) < 4, F.concat(F.lit("0"), F.col('TIME_OCC')))
                                        .otherwise(F.col('TIME_OCC'))) \
            .withColumn("TIME_OCC", F.concat(F.col("TIME_OCC")[0:2], F.lit(":"), F.col("TIME_OCC")[3:4]))


    #format data with sql
    df.createOrReplaceTempView('CRIMES_TEMP')

    query_format = """
        SELECT
            DR_NO AS CRIME_ID,
            TO_DATE(Date_Rptd) AS DATE_REPORTED,
            TO_DATE(DATE_OCC) AS DATE_OCCURRENCE,
            TIME_OCC AS TIME_OCCURRENCE,
            CAST(AREA AS INT) AS AREA_ID,
            AREA_NAME,
            CAST(Rpt_Dist_No AS INT) AS REPORT_DISTRICT_ID,
            CAST(Crm_Cd AS INT) AS CRIME_TYPE_ID,
            Crm_Cd_Desc AS CRIME_TYPE_DESCRIPTION,
            CAST(Vict_Age AS INT) AS VICTIM_AGE,
            Vict_Sex AS VICTIM_SEX,
            Vict_Descent AS VICTIM_DESCENT,
            CAST(Premis_Cd AS INT) AS PREMIS_ID,
            Premis_Desc AS PREMIS_DESCRIPTION,
            CAST(Weapon_Used_Cd AS INT) AS WEAPON_ID,
            Weapon_Desc AS WEAPON_DESCRIPTION,
            Status AS CRIME_STATUS_ID,
            Status_Desc AS CRIME_STATUS_DESCRIPTION,
            CAST(Crm_Cd_1 AS INT) AS ADDITIONAL_CRIME_ID_1,
            CAST(Crm_Cd_2 AS INT) AS ADDITIONAL_CRIME_ID_2,
            CAST(Crm_Cd_3 AS INT) AS ADDITIONAL_CRIME_ID_3,
            CAST(Crm_Cd_4 AS INT) AS ADDITIONAL_CRIME_ID_4,
            LOCATION AS LOCATION_NAME,
            CAST(LAT AS FLOAT) AS LOCATION_LATITUDE,
            CAST(LON AS FLOAT) AS LOCATION_LONGITUDE
        FROM CRIMES_TEMP
    """

    df_format = spark.sql(query_format)



    #create pandas df
    pandas_df = df_format.toPandas()


    #export data
    return pandas_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
