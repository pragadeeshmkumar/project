import logging
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.exceptions import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Read and log request details
            request_body = await request.body()
            logger.info(f"Request: {request.method} {request.url}\nHeaders: {dict(request.headers)}\nBody: {request_body.decode('utf-8', errors='replace')}")
            
            # Proceed with the request and get the response
            response = await call_next(request)

            # Attempt to read the response body
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            
            # Log response details
            logger.info(f"Response: {response.status_code} {response.headers}\nBody: {response_body.decode('utf-8', errors='replace')}")
            
            # Return the response with the original body
            return Response(content=response_body, status_code=response.status_code, headers=dict(response.headers))

        except Exception as e:
            # Log the error details
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
            # Optionally re-raise the error or handle it as needed
            raise HTTPException(status_code=500, detail="An internal server error occurred.")

