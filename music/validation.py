from werkzeug.exceptions import HTTPException
from flask import make_response,jsonify

class NotFoundError(HTTPException):
    def __init__(self,status_code):
        
        self.response= make_response("",status_code)

class ValidationError(HTTPException):
    def __init__(self,error_code,error_message,status_code):
        
        message={
                    "error_code":error_code,
                    "error_message":error_message
                }
        
        self.response= make_response(jsonify(message),status_code)
