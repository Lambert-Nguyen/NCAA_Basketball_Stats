from typing import Any, Dict, Optional
from src.app.req_res import StdResponse
from src.utils.status_codes import StatusCodes
from src.utils.errors import CustomException

class ErrorHandler:
    """Centralized error handler for API endpoints"""
    
    @staticmethod
    def handle_error(error: Exception, success_message: str = "Operation successful") -> StdResponse:
        """
        Handle exceptions and return appropriate StdResponse
        
        Args:
            error: The exception that was raised
            success_message: Message to return when no error occurs
            
        Returns:
            StdResponse object with appropriate error handling
        """
        if isinstance(error, CustomException):
            return StdResponse(
                message=error.message,
                error=error.message,
                data=None,
                status_code=error.status_code,
                success=False
            )
        
        # Handle unexpected errors
        return StdResponse(
            message="An unexpected error occurred",
            error=str(error),
            data=None,
            status_code=StatusCodes.INTERNAL_SERVER_ERROR.value,
            success=False
        )
    
    @staticmethod
    def handle_success(data: Optional[Dict[str, Any]] = None, message: str = "Operation successful") -> StdResponse:
        """
        Handle successful operations and return appropriate StdResponse
        
        Args:
            data: Optional data to return with the response
            message: Success message to return
            
        Returns:
            StdResponse object for successful operations
        """
        return StdResponse(
            message=message,
            error="",
            data=data,
            status_code=StatusCodes.SUCCESS.value,
            success=True
        ) 