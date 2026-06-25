import logging
import os
import pandas as pd
import numpy as np
from pyparsing import col
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            logger.info(f"Created directory: {self.processed_dir}")



    def preprocess_data(self,df):
        try:
            logger.info("Starting data preprocessing step")
            logger.info(f"Dropping columns")
            df.drop(columns=['Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]
            logger.info(f"Applying Label Encoding")


            label_encoder = LabelEncoder()

            mappings={}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])

                mappings[col] = {label:code for label,code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}

            logging.info(f"Label mappings")    
            for col, map in mappings.items():
                logging.info(f"{col}: {map}")


            logger.info("Skewness Handling")
            skew_threshold = self.config["data_processing"]["skewness_threshold"]    
            skewness = df[num_cols].apply(lambda x:x.skew())

            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column])
            return df     
        except Exception as e:
            logger.error(f"Error in data preprocessing: {e}")
            raise CustomException("Data preprocessing failed", e)
        

    def balance_data(self, df):
        try:
            logger.info("Handling Imbalanced Data")
            X = df.drop(columns='booking_status')
            y = df['booking_status']
            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)
            balanced_df = pd.DataFrame(X_resampled , columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Successfully balanced the dataset using SMOTE")
            return balanced_df
        except Exception as e:
            logger.error(f"Error in balancing data: {e}")
            raise CustomException("Data balancing failed", e)
        

    def select_features(self, df):
        try:
            logger.info("Starting feature selection step")
            X = df.drop(columns='booking_status')
            y = df['booking_status']
            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)
            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({'feature': X.columns, 'importance': feature_importance})
            top_features_importance_df= feature_importance_df.sort_values(by='importance', ascending=False)
            num_features_to_select = self.config["data_processing"]["no_of_features"]
            top_10_features = top_features_importance_df["feature"].head(num_features_to_select).values
            logger.info(f"Top {num_features_to_select} features selected: {top_10_features}")
            top_10_df = df[top_10_features.tolist() + ["booking_status"]]
            logger.info(f"Selected top {num_features_to_select} features based on importance")
            return top_10_df
        except Exception as e:
            logger.error(f"Error in feature selection: {e}")
            raise CustomException("Feature selection failed", e)    
        
    def save_data(self, df, file_path):
        try:
            logger.info(f"Saving processed data to {file_path}")
            df.to_csv(file_path, index=False)
            logger.info(f"Successfully saved processed data to {file_path}")
        except Exception as e:
            logger.error(f"Error saving data to {file_path}: {e}")
            raise CustomException(f"Failed to save data to {file_path}", e)    
        

    def process(self):
        try:
            logger.info("Loading data from RAW directory")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]  # Ensure test_df has the same columns as train_df

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)
            logger.info("Data processing completed successfully")
        except Exception as e:
            logger.error(f"Error in data processing: {e}")
            raise CustomException("Data processing failed", e)
        


if __name__ == "__main__":
    processor = DataProcessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PROCESSED_DIR,
        config_path=CONFIG_PATH
    )
    processor.process()        

