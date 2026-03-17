import os
import polars as pl
from src.etl.base_classes import Loader

class ParquetLoader(Loader):
    def load(self, df: pl.DataFrame, destination: str) -> None:
        if df.is_empty():
            return
            
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        df.write_parquet(destination)
