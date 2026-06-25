import os
import sys
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml


logger = get_logger(__name__)


class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"DataIngestion initialized with bucket: {self.bucket_name}, file: {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client(project=self.config["project_id"])
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"CSV file is Successfully Downloaded {self.file_name} from GCP bucket {self.bucket_name} to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error downloading file from GCP: {str(e)}")
            raise CustomException(f"Error downloading file from GCP: {str(e)}",sys)    
        

    def split_data(self):
        try:
            logger.info(f"Starting data split with train-test ratio: {self.train_test_ratio}")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size=1 - self.train_test_ratio, random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)
            logger.info(f"Data successfully split into train and test sets with ratio {self.train_test_ratio}")
        except Exception as e:
            logger.error(f"Error splitting data: {str(e)}")
            raise CustomException(f"Failed to split data into training and test sets: {str(e)}",sys)    
        


    def run(self):
        try:
            logger.info("Starting data ingestion process...")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data ingestion process completed successfully.")
        except Exception as e:
            logger.error(f"Data ingestion process failed: {str(e)}")
            raise CustomException(f"Data ingestion process failed: {str(e)}",sys)    
        
        finally:
            logger.info("Data ingestion process finished.")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()