from pydantic import BaseModel


class FileSettings(BaseModel):
    default_format: str = "csv"
    infer_schema: bool = True
    header: bool = True
    delimiter: str = ","


class PlusFrameConfig(BaseModel):
    file_handling: FileSettings
