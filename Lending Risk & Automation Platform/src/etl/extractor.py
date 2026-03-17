import json
import logging
import httpx
import asyncio
from typing import List, Dict, Any
from src.etl.base_classes import Extractor

logger = logging.getLogger(__name__)

class APIExtractor(Extractor):
    def __init__(self, api_url: str, watermark_path: str):
        self.api_url = api_url
        self.watermark_path = watermark_path
        self.watermark = self._load_watermark()

    def _load_watermark(self) -> str:
        try:
            with open(self.watermark_path, 'r') as f:
                return json.load(f).get("last_updated", "2000-01-01T00:00:00")
        except FileNotFoundError:
            return "2000-01-01T00:00:00"

    async def _fetch(self, since: str, limit: int) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {"since": since, "limit": limit}
            response = await client.get(f"{self.api_url}/loans", params=params)
            response.raise_for_status()
            return response.json()

    def extract(self, limit: int = 100) -> List[Dict[str, Any]]:
        # Using loop.run_until_complete if not already in a loop, 
        # but better to handle async at orchestrator level.
        # For this refactor, we'll assume the orchestrator handles the async loop.
        return asyncio.run(self._fetch(self.watermark, limit))
