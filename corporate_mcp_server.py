"""
Corporate MCP Server Module

This module implements a FastMCP server that exposes corporate data tools.
It manages a local SQLite database containing employee records and internal
documents, and provides search and analytics capabilities to MCP clients.
"""

import sqlite3
import json

from fastmcp import FastMCP
from logger_config import setup_logger


logger = setup_logger(__name__)

mcp = FastMCP("Corporate System")


def get_db_connection():
    """
    Summary:
        Creates and returns a SQLite database connection with row factory enabled.

    Args:
        None

    Returns:
        sqlite3.Connection: An active SQLite database connection.
    """
    try:
        logger.debug("Opening database connection to corporate.db")
        conn = sqlite3.connect("corporate.db")
        conn.row_factory = sqlite3.Row
        return conn
    except Exception:
        logger.exception("Failed to create database connection")
        raise


def init_sample_db():
    """
    Summary:
        Initializes the corporate database schema and inserts sample data
        if it does not already exist.

    Args:
        None

    Returns:
        None
    """
    try:
        logger.info("Initializing corporate database with sample data")

        conn = sqlite3.connect("corporate.db")
        cursor = conn.cursor()

        logger.debug("Creating database tables if they do not exist")

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS employees
               (id INTEGER PRIMARY KEY, name TEXT, department TEXT, email TEXT)"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS documents
               (id INTEGER PRIMARY KEY, title TEXT, content TEXT, category TEXT)"""
        )

        logger.debug("Inserting sample employee records")
        cursor.execute(
            "INSERT OR IGNORE INTO employees VALUES (1, 'John Doe', 'Engineering', 'john@company.com')"
        )
        cursor.execute(
            "INSERT OR IGNORE INTO employees VALUES (2, 'Jane Smith', 'Sales', 'jane@company.com')"
        )
        cursor.execute(
            "INSERT OR IGNORE INTO employees VALUES (3, 'Bob Wilson', 'Engineering', 'bob@company.com')"
        )

        logger.debug("Inserting sample document records")
        cursor.execute(
            "INSERT OR IGNORE INTO documents VALUES (1, 'Q4 Sales Report', 'Sales increased by 20% in Q4 2024...', 'reports')"
        )
        cursor.execute(
            "INSERT OR IGNORE INTO documents VALUES (2, 'Engineering Guidelines', 'Follow these coding standards...', 'guidelines')"
        )
        cursor.execute(
            "INSERT OR IGNORE INTO documents VALUES (3, 'HR Policy', 'Employee benefits and policies...', 'hr')"
        )

        conn.commit()
        conn.close()

        logger.info("Corporate database initialization completed successfully")

    except Exception:
        logger.exception("Failed to initialize corporate database")
        raise


# Initialize database at startup
init_sample_db()


@mcp.tool()
def search_documents(query: str) -> str:
    """
    Summary:
        Searches corporate documents by title, content, or category.

    Args:
        query: Search query string.

    Returns:
        A JSON-formatted string containing matching documents or
        a message if no documents are found.
    """
    try:
        logger.info("Searching documents")
        logger.debug(f"Document search query: {query}")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM documents
            WHERE title LIKE ? OR content LIKE ? OR category LIKE ?
            """,
            (f"%{query}%", f"%{query}%", f"%{query}%"),
        )

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        if not results:
            logger.info("No documents found")
            return f"No documents found matching '{query}'"

        logger.info(f"Found {len(results)} document(s)")
        return json.dumps(results, indent=2)

    except Exception:
        logger.exception("Error occurred while searching documents")
        raise


@mcp.tool()
def query_employees(query: str) -> str:
    """
    Summary:
        Searches employee records by name, department, or email.

    Args:
        query: Employee name, department, or email to search for.

    Returns:
        A JSON-formatted string containing matching employees or
        a message if no employees are found.
    """
    try:
        logger.info("Searching employee records")
        logger.debug(f"Employee search query: {query}")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM employees
            WHERE name LIKE ? OR department LIKE ? OR email LIKE ?
            """,
            (f"%{query}%", f"%{query}%", f"%{query}%"),
        )

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        if not results:
            logger.info("No employees found")
            return f"No employees found matching '{query}'"

        logger.info(f"Found {len(results)} employee(s)")
        return json.dumps(results, indent=2)

    except Exception:
        logger.exception("Error occurred while querying employees")
        raise


@mcp.tool()
def get_department_stats(department: str) -> str:
    """
    Summary:
        Retrieves employee count statistics for a specific department.

    Args:
        department: Department name to retrieve statistics for.

    Returns:
        A JSON-formatted string containing department statistics.
    """
    try:
        logger.info("Fetching department statistics")
        logger.debug(f"Department requested: {department}")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) as employee_count
            FROM employees
            WHERE department LIKE ?
            """,
            (f"%{department}%",),
        )

        result = dict(cursor.fetchone())
        conn.close()

        logger.info("Department statistics retrieved successfully")
        return json.dumps(
            {
                "department": department,
                "employee_count": result["employee_count"],
            },
            indent=2,
        )

    except Exception:
        logger.exception("Error occurred while fetching department statistics")
        raise


if __name__ == "__main__":
    logger.info("Starting Corporate MCP server")
    mcp.run(transport="stdio")
