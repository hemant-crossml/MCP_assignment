"""
Corporate Assistant Application Entry Point

This module serves as the main entry point for running the corporate
assistant powered by LangChain and FastMCP. It initializes the agent,
handles user interaction, and manages the async event loop lifecycle.
"""

import asyncio

from client import client
from agent import create_corporate_agent
from logger_config import setup_logger


logger = setup_logger(__name__)


async def main():
    """
    Summary:
        Initializes the corporate agent and runs an interactive
        command-line session for user interaction.

    Args:
        None

    Returns:
        None
    """
    logger.info("Starting Corporate Assistant application")
    print("--- Corporate Assistant (LangChain + FastMCP) ---")

    try:
        logger.info("Creating corporate agent")
        agent = await create_corporate_agent(client)
        logger.info("Corporate agent initialized successfully")

        print("Assistant ready. Type 'exit' to quit.")

        while True:
            user_input = input("\nYou: ")
            logger.debug(f"User input received: {user_input}")

            if user_input.lower() in ["exit", "quit"]:
                logger.info("Exit command received from user")
                break

            logger.debug("Invoking agent with user input")
            result = await agent.ainvoke(
                {"messages": [("human", user_input)]}
            )

            response = result["messages"][-1].content
            logger.debug("Agent response generated")

            print(f"\nAssistant: {response}")

        logger.info("User session ended gracefully")

    except Exception:
        logger.exception("Unhandled exception occurred in main application loop")
        print("An unexpected error occurred. Please check logs for details.")


if __name__ == "__main__":
    try:
        logger.info("Launching asyncio event loop")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user (KeyboardInterrupt)")
        print("\nClosing connection...")
    except Exception:
        logger.exception("Fatal error during application startup")
        raise
