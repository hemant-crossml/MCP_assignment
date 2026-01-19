"""
LangChain Agent Initialization Module

Summary:
This module is responsible for initializing a LangChain agent using a
preconfigured language model and a set of custom tools.

Description:
- Imports a language model client.
- Registers tools for terminal command execution, web search, and
  automated Python test case generation.
- Sets up structured logging.
- Creates and validates a LangChain agent instance with proper
  error handling and logging for observability.

If agent creation fails, the error is logged with stack trace details
and re-raised to ensure failure visibility.
"""

from langchain.agents import create_agent

from prompt import system_prompt
from client import model
from logger_config import setup_logger


logger = setup_logger(__name__)


async def create_corporate_agent(client):
    """
    Summary:
        Retrieves tools from the MCP server and creates a LangChain agent
        using the configured language model and system prompt.

    Args:
        client: MCP client instance used to fetch available tools.

    Returns:
        A fully initialized LangChain agent instance.
    """
    logger.info("Starting corporate agent creation")

    try:
        logger.debug("Fetching tools from MCP client")
        tools = await client.get_tools()
        logger.info("Tools successfully retrieved from MCP client")
        logger.debug(f"Retrieved tools: {tools}")

        logger.info("Creating LangChain agent instance")
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=system_prompt
        )

        logger.info("LangChain agent created successfully")
        return agent

    except Exception:
        logger.exception("Failed to create corporate agent")
        raise
