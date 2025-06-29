
import logging

def get_logger(name):
   
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Create file handler
        file_handler = logging.FileHandler("employee_api.log")
        
        # Create console handler for immediate feedback
        console_handler = logging.StreamHandler()
        
        # Create a detailed formatter
        detailed_format = '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(funcName)s() | [%(threadName)s] | %(message)s'
        # Use a simpler date format that's compatible with the standard library
        formatter = logging.Formatter(detailed_format, datefmt='%Y-%m-%d %H:%M:%S')
        
        # Set formatter for both handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Set log level
        logger.setLevel(logging.INFO)
    return logger
