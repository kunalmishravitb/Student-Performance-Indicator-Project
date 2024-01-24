# Logger is for the purpose that any execution that probably happens it should be able to log all those information in some files so that we will be able to track if there are some errors like custom exception errors so that we will log in the text file.


import logging
import os
from datetime import datetime

# Creating our log file
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #%m_%d_%Y_%H_%M_%S means month, day, year, hour, minute, second

# A folder named "logs" will get created with respect to current working directory
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)

# Even though there is a file / folder keep on appending the files inside that whenever we want to create a file
os.makedirs(logs_path,exist_ok=True)


LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

# Setting the logging function in the basic config so that we can override the functionality of logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


# This code is only for checking if your logger.py is running or not by typing: python src/logger.py
#if __name__=="__main__":
#    logging.info("Logging has started")
