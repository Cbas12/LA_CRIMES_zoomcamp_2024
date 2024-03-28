from pyspark.sql import types
from pyspark.sql import functions as F

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    #print(data)
    spark = kwargs.get('spark')

    #data.createOrReplaceTempView('CRIMES')

    #query = (
    #    "SELECT * FROM CRIMES"
    #)

    #query_results = spark.sql(query)

    #print(query_results)

    
    return "mierda"


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
