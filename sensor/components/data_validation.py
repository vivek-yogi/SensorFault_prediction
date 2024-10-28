from distutils import dir_util
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml,write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os,sys

class DataValidation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config  = data_validation_config
            self._schema_config          = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)
        
    def drop_zero_std_columns(self,dataframe):
        pass

    def validate_number_of_columns(self,dataframe:pd.DataFrame) ->bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f'Required number of columns: {number_of_columns}')
            logging.info(f'Data frame has columns:{len(dataframe.columns)}')

            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e,sys)
        

    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config['numerical_columns']
            dataframe_columns = dataframe.columns
            numerical_column_present  = True
            missing_numerical_columns = []

            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_columns.append(num_column)
            
            logging.info(f"Missing numerical columns:[{missing_numerical_columns}]")
            
            return numerical_column_present
        
        except Exception as e:
            raise SensorException(e,sys)


    @staticmethod
    def read_data(file_path) ->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try: 
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),"drift_status":is_found}})
            
            # create directory
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return status
        except Exception as e:
            raise SensorException(e,sys)



    def initiate_data_validation(self)->DataIngestionArtifact :
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path  = self.data_ingestion_artifact.test_file_path

            # reading data from train and test file loction

            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe  = DataValidation.read_data(test_file_path)    

            # validate no of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message += "Number of columns in train dataframe does not match with the expected schema.\n"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message += "Number of columns in test dataframe does not match with the expected schema.\n"

            # validate numerical columns
            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message += "Numerical columns in train dataframe are not present in the expected schema.\n"
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message += "Numerical columns in test dataframe are not present in the expected schema.\n"

            if len(error_message) > 0:
                raise SensorException(error_message,sys)
            
            # detect dataset drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            if not status:
                error_message += "Dataset drift detected between train and test datasets.\n"

            data_validation_artifact = DataValidationArtifact(
                validation_status       = status,
                valid_train_file_path   = self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path    = self.data_ingestion_artifact.test_file_path,
                drift_report_file_path  = self.data_validation_config.drift_report_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path  = None,

            )

            logging.info(f"Data validation artifact: {DataValidationArtifact}")
            return data_validation_artifact
        
        except Exception as e:
            raise SensorException(e,sys)