from rest_framework.response import Response
from rest_framework import status

class BaseResponseMixin:
    def success_response(self, data=None, message="Success", code=status.HTTP_200_OK):
        return Response({
            "success": True,
            "statusCode": code,
            "message": message,
            "data": data
        }, status=status.HTTP_200_OK)

    def error_response(self, errors = None, message="Failed", code=status.HTTP_400_BAD_REQUEST):
        return Response({
            "success": False,
            "statusCode": code,
            "message": message,
            "errors" :  errors,
            "data": None
        }, status=code)
