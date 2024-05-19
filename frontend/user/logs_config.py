import logging

# Setup custom logging, terminal and file logging
def setup_logging(log_terminal = False):
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the logging level
    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add a FileHandler, so our logs will be store in a file, such that we can trace errors, and recreate bugs.
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)  # Set the logging level for the file
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # For easy debugging, 
    if log_terminal:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Set the logging level for the console
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger