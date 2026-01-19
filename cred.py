import os
from dotenv import load_dotenv

from logger_config import setup_logger

# Initialize logger for this module
logger = setup_logger(__name__)

logger.info("Starting credential loading process")

# Load variables from .env file into environment
load_dotenv()
logger.debug(".env file loaded successfully")

# Read Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
logger.debug(f"GEMINI_API_KEY present: {bool(GEMINI_API_KEY)}")

# Validate API key existence
if not GEMINI_API_KEY:
    logger.critical("GEMINI_API_KEY not found in .env file")
    raise EnvironmentError("GEMINI_API_KEY not found in .env file")

logger.info("All required API keys validated successfully")