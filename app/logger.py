import logging
from starlette.requests import Request
from starlette.responses import Response

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def log_request_response(request: Request, response: Response):
    logger.info(f"Request: {request.method} {request.url} {request.headers}")
    logger.info(f"Response: {response.status_code} {response.headers}")
