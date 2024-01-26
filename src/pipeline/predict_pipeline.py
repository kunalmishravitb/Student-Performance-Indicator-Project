# This is for prediction purposes.
# A simple web application will be created which will be interacting with various pickle files with respect to any input data that we will give in the form.


import sys # Used for exception handling
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass
    
    # This predict is just like model prediction
    def predict(self, features):
        try:
            model_path=os.path.join("artifacts", "model.pkl")
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl') # This preprocessor is responsible in handling categorical features, for doing feature scaling
            print("Before Loading")
            model=load_object(file_path=model_path) # load_object will just load the pickle file in short
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading")
            data_scaled=preprocessor.transform(features) # Scaling the data
            preds=model.predict(data_scaled) # Prediction
            return preds 
        except Exception as e:
            raise CustomException(e, sys)


# CustomData class will be responsible in mapping all the inputs that we are giving in html to the backend with this particular values
class CustomData:
    def __init__(self,
                 gender: str,
                 race_ethnicity: str,
                 parental_level_of_education: str,
                 lunch: str,
                 test_preparation_course: str,
                 reading_score: int,
                 writing_score: int):
        self.gender=gender
        self.race_ethnicity=race_ethnicity
        self.parental_level_of_education=parental_level_of_education
        self.lunch=lunch
        self.test_preparation_course=test_preparation_course
        self.reading_score=reading_score
        self.writing_score=writing_score
    

    # This function will return all our input in the form of a dataframe
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict={
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)
