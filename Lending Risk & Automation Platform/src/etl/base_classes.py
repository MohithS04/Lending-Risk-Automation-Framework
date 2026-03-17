from abc import ABC, abstractmethod
from typing import Any, Dict, List
import polars as pl

class Extractor(ABC):
    @abstractmethod
    def extract(self) -> List[Dict[str, Any]]:
        pass

class Transformer(ABC):
    @abstractmethod
    def transform(self, data: List[Dict[str, Any]]) -> pl.DataFrame:
        pass

class Loader(ABC):
    @abstractmethod
    def load(self, df: pl.DataFrame, destination: str) -> None:
        pass
