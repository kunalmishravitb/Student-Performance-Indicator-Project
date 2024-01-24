import sys # any exception that is basically getting controlled the sys library automatically will have that information
from src.logger import logging # used for saving the message in the logs folder


# This is the function that define how your messsage will look like inside the file with respect to custom exception
# Whenever an exception gets raised I have to push as my own custom message
def error_message_detail(error,error_detail:sys): # here error_detail will basically be present inside the sys
    _,_,exc_tb=error_detail.exc_info() # this is basically talking about execution info. This will give you three important information. So we are not interested in first two information but the last information will basically give about on which file the exception has occurred, on which line number the exception has occurred and so on. So all this information will be stored in the exec_info().
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error) # exc_tb means execution tab
    )

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys): # __init__ is the constructor
        super().__init__(error_message) # we are inheriting from the exception
        self.error_message=error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message # whenever I will try to print it I will get all the error message


# This code is only for checking if your exception.py is running or not by typing: python src/exception.py
#if __name__=="__main__":
#    logging.info("Logging has started")

#    try:
#        a=1/0
#    except Exception as e:
#        logging.info('Division by zero')
#        raise CustomException(e,sys)
