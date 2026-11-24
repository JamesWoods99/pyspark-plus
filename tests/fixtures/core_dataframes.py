from pyspark.sql import SparkSession
from pytest import fixture


@fixture
def mock_df_base(spark: SparkSession):
    data = [
        (1, "Mark"),
        (2, "John"),
        (3, "Luke"),
        (4, "Matthew"),
    ]

    return spark.createDataFrame(
        data,
        ["id", "name"],
    )
