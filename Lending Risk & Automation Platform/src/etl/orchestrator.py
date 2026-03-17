import yaml
import os
import json
import logging
from datetime import datetime
from src.etl.extractor import APIExtractor
from src.etl.transformer import LoanTransformer
from src.etl.loader import ParquetLoader

logger = logging.getLogger("ETLOrchestrator")

class ETLOrchestrator:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.extractor = APIExtractor(
            api_url=self.config['api']['url'],
            watermark_path=self.config['api']['watermark_path']
        )
        self.transformer = LoanTransformer()
        self.loader = ParquetLoader()

    def run(self):
        logger.info("Starting ETL Pipeline run")
        try:
            # 1. Extract
            raw_data = self.extractor.extract(limit=self.config['pipeline']['batch_size'])
            if not raw_data:
                logger.info("No data to process.")
                return

            # 2. Transform
            df = self.transformer.transform(raw_data)
            logger.info(f"Transformed {df.height} records.")

            # 3. Load
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"processed_loans_{datetime.now().strftime('%H%M%S')}.parquet"
            dest = os.path.join(self.config['pipeline']['processed_dir'], today, filename)
            
            self.loader.load(df, dest)
            logger.info(f"Loaded data to {dest}")

            # 4. Update Watermark
            max_updated = df["updated_at"].max().isoformat()
            with open(self.config['api']['watermark_path'], 'w') as f:
                json.dump({"last_updated": max_updated}, f)
            logger.info(f"Updated watermark to {max_updated}")

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    orchestrator = ETLOrchestrator("config/pipeline_config.yaml")
    orchestrator.run()
