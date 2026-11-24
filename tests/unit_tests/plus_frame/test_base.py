from pyspark.sql import DataFrame

from pyspark_plus.plus_frame.base import PlusFrame


def test_working(mock_df_base: DataFrame):
    PlusFrame(mock_df_base)
