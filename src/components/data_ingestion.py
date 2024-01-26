# Reading a dataset from a specific database or it can be some other file location is called data ingestion.
# We will divide the dataset into train and test while reading the data.


import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer



# Because of this Decorator you will be able to directly define class variable
@dataclass

# In my data ingestion component any input that is required I will probably give through this data ingestion config
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts', "train.csv") # Data Ingestion components output will saved all the files in this path
    test_data_path: str=os.path.join('artifacts', "test.csv")
    raw_data_path: str=os.path.join('artifacts', "data.csv")


class DataIngestion: # Whenever I will call DataIngestion class then the above three path will be saved inside the DataIngestionConfig variable 
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    # If my data is stored in some databases then I will write my code over here to read from the database
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv('notebook\data\stud.csv') # Reading the dataset
            logging.info('Read the dataset as dataframe')

            # Creating the artifacts folder
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True) # If the folder is already there then we have to keep that folder and we don't have to delete it and again create it
            
            # Saving the raw data path inside the artifacts folder
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            train_set, test_set=train_test_split(df, test_size=0.2, random_state=42)

            # Saving the train data path inside the same artifacts folder
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)

            # Saving the test data path inside the same artifacts folder
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            # Here we are returning the train data path and test data path to my next step which is basically data transformation
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)
        
# Initiating so that we can run data_ingestion.py by writing the code: python src/components/data_ingestion.py
if __name__=="__main__":
    # Calling the DataIngestion class
    obj=DataIngestion()
    train_data, test_data=obj.initiate_data_ingestion()

    # Calling the DataTranformation class
    data_transformation=DataTransformation()
    train_arr, test_arr, _=data_transformation.initiate_data_transformation(train_data, test_data) # As we have already created the pickle file so we don't want to assign the last one so we have given _

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))
