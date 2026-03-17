import os
import json
import logging
import asyncio
from datetime import datetime
from typing import List, Dict, Any
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from logging.handlers import RotatingFileHandler

# Configure Logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(os.path.join(log_dir, "ingestion.log"), maxBytes=10**6, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("IngestionEngine")

class LendingDataIngestor:
    def __init__(self, api_url: str, watermark_path: str, raw_data_dir: str):
        self.api_url = api_url
        self.watermark_path = watermark_path
        self.raw_data_dir = raw_data_dir
        self.watermark = self._load_watermark()

    def _load_watermark(self) -> str:
        if os.path.exists(self.watermark_path):
            with open(self.watermark_path, 'r') as f:
                return json.load(f).get("last_updated", "2000-01-01T00:00:00")
        return "2000-01-01T00:00:00"

    def _save_watermark(self, timestamp: str):
        with open(self.watermark_path, 'w') as f:
            json.dump({"last_updated": timestamp}, f)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(httpx.HTTPError)
    )
    async def fetch_data(self, client: httpx.AsyncClient, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        logger.info(f"Fetching data from {self.api_url} with params: {params}")
        response = await client.get(f"{self.api_url}/loans", params=params)
        response.raise_for_status()
        return response.json()

    async def ingest(self, limit: int = 100):
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                params = {
                    "since": self.watermark,
                    "limit": limit
                }
                
                records = await self.fetch_data(client, params)
                
                if not records:
                    logger.info("No new records found.")
                    return

                # Deduce new watermark
                max_updated = max(r['updated_at'] for r in records)
                
                # Store partitioned data
                today = datetime.now().strftime("%Y-%m-%d")
                partition_dir = os.path.join(self.raw_data_dir, today)
                os.makedirs(partition_dir, exist_ok=True)
                
                filename = f"loans_{datetime.now().strftime('%H%M%S')}.json"
                filepath = os.path.join(partition_dir, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(records, f, indent=4)
                
                self._save_watermark(max_updated)
                logger.info(f"Successfully ingested {len(records)} records into {filepath}")
                logger.info(f"Updated watermark to {max_updated}")

            except Exception as e:
                logger.error(f"Ingestion failed: {e}", exc_info=True)

async def main():
    API_URL = "http://localhost:8000"
    WATERMARK_FILE = "config/watermark.json"
    RAW_DATA_DIR = "data/raw"
    
    ingestor = LendingDataIngestor(API_URL, WATERMARK_FILE, RAW_DATA_DIR)
    await ingestor.ingest(limit=50)

if __name__ == "__main__":
    asyncio.run(main())
