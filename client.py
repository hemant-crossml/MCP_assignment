"""
Client and Model Initialization Module

This module initializes and exposes:
- A MultiServer MCP client used to communicate with the corporate MCP server.
- A Google Gemini language model configured with application settings.

Both objects are created at import time and are intended to be reused
across the application.
"""

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI

from cred import GEMINI_API_KEY
from config import *
from logger_config import setup_logger


logger = setup_logger(__name__)


try:
    logger.info("Initializing MultiServer MCP client")

    client = MultiServerMCPClient(
        {
            "corporate_system": {
                "command": "python",
                "args": ["corporate_mcp_server.py"],
                "transport": "stdio"
            }
        }
    )

    logger.info("MultiServer MCP client initialized successfully")
    logger.debug("MCP client configured for corporate_system via stdio")

except Exception:
    logger.exception("Failed to initialize MultiServer MCP client")
    raise


try:
    logger.info("Initializing Google Gemini language model")

    model = ChatGoogleGenerativeAI(
        model=MODEL_ID,
        api_key=GEMINI_API_KEY,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        top_k=TOP_K,
        max_output_tokens=MAX_TOKEN,  # output length cap
    )

    logger.info("Google Gemini language model initialized successfully")
    logger.debug(
        "Model configuration loaded "
        f"(MODEL_ID={MODEL_ID}, TEMPERATURE={TEMPERATURE}, "
        f"TOP_P={TOP_P}, TOP_K={TOP_K}, MAX_TOKEN={MAX_TOKEN})"
    )

except Exception:
    logger.exception("Failed to initialize Google Gemini language model")
    raise
