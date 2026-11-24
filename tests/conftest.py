from pathlib import Path
from pkgutil import walk_packages

import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark() -> SparkSession:  # type: ignore
    session = (
        SparkSession.builder.master("local[2]")
        .appName("pyspark-plus-tests")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
    )

    yield session  # type: ignore

    session.stop()


FIXTURES_PACKAGE = "tests.fixtures"
FIXTURES_PATH = Path(__file__).parent / "fixtures"

pytest_plugins = [
    module.name
    for module in walk_packages(
        [str(FIXTURES_PATH)],
        prefix=f"{FIXTURES_PACKAGE}.",
    )
    if not module.ispkg and not module.name.rsplit(".", 1)[-1].startswith("_")
]
