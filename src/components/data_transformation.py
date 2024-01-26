# Here we will write code related to how to change categorical features into numerical features, how to handle One-Hot Encoding or Label Encoding.


import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer # This library is basically used to create pipeline
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object


@dataclass
class DataTransformationConfig: # It will give me any path that will be required, or any inputs I probably will be requiring for data transmission components
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl") # ceate any models and saved in the pickle path


# This is the input that probably we will be giving
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    

    # This function will basically create pickle file which will basically be responsible for converting categorical features into numerical features or performing standard scaler and all
    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            numerical_columns=["writing_score", "reading_score"]
            categorical_columns=[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            # This Pipeline should run on the training dataset
            num_pipeline=Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")), # Handling the missing values with the help of median
                    ("scaler", StandardScaler()) # Doing Standard Scaling
                ]
            )

            cat_pipeline=Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")), # Replacing all the missing values with the help of mode
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # Combining numerical pipeline with categorical pipeline together
            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipelines", cat_pipeline, categorical_columns)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
    

    # Starting data transformation process inside this function
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_columns=["writing_score", "reading_score"]

            # Dropping the target column from the input features
            input_feature_train_df=train_df.drop(columns=[target_column_name], axis=1)
            
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr=np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr=np.c_[input_feature_test_arr, np.array(target_feature_test_df)] # Using np.c_ we are basically combining

            logging.info(f"Saved preprocessing object.")

            # With the help of this code in data transformation we are saving this pickle name in the hard disk
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)