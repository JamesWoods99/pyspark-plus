import os
from unittest.mock import MagicMock

env_name = "DATABRICKS_RUNTIME_VERSION"

if os.environ.get(env_name) is not None:
    try:
        dbutils  # type: ignore  # noqa: B018, F821
        display  # type: ignore  # noqa: B018, F821
    except Exception:  # noqa: BLE001
        dbutils = MagicMock()
        display = MagicMock()
else:
    dbutils = MagicMock()
    display = MagicMock()
