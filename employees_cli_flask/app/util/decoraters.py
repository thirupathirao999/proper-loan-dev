"""Utility decorators for the Employee API application.

This module provides decorator functions that can be applied to routes and service
functions to add cross-cutting functionality like error handling, logging, and
performance monitoring.
"""

from functools import wraps
import time
from flask import jsonify, request
from app.util.logger import get_logger

# Initialize logger
logger = get_logger('employee_api.decorators')

def time_execution_logger(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        try:

            start_time = time.time()            
            result, status_code =  func(*args, **kwargs)
            end_time = time.time()
            execution_time_ms = round ((end_time - start_time) * 1000,2)

            if isinstance(result,dict):
                result['execution_time_ms'] = execution_time_ms
            else:
                 data = result.get_json()
                 if isinstance(data,list):
                    data = {'data': data, 'execution_time_ms' : execution_time_ms }
                 elif isinstance(data,dict):
                     result['execution_time_ms'] = execution_time_ms
                 else:
                     data = {'data': data, 'execution_time_ms' : execution_time_ms }


            result = jsonify(data)
            return result, status_code
        
        except Exception as e:
            return jsonify({"Error" : str(e) }), 500
    return wrapper


def handle_exceptions(func):
    """Decorator that catches and handles exceptions raised by the decorated function.
    
    This decorator wraps a function to catch any exceptions that might be raised
    during its execution. If an exception occurs, it returns a JSON response with
    a 500 status code and the error message, preventing the application from crashing.
    
    Args:
        func (callable): The function to decorate.
        
    Returns:
        callable: The wrapped function that handles exceptions.
        
    Example:
        @handle_exceptions
        def load_data():
            # This function will not crash the application if it fails
            # Instead, it will return a JSON error response
            return process_data()
    """
    @wraps(func)
    def wrapper (*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({"Error" : str(e) }), 500
    return wrapper


