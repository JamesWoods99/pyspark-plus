from pyspark.sql import DataFrame, SparkSession

from ._file_handling import FileHandling


class PlusFrame:
    # Base
    df: DataFrame
    spark: SparkSession

    # Modules
    file_handling: FileHandling

    def __init__(self, df: DataFrame):
        self._df = df
        self.spark = SparkSession.builder.getOrCreate()

        # Modules
        self.file_handling = FileHandling(self)

    def __getattr__(self, name):
        return getattr(self._df, name)
