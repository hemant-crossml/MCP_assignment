import sqlite3
import json


from fastmcp import FastMCP

mcp = FastMCP("Corporate System")

def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect('corporate.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_sample_db():
    """Initialize sample corporate database."""
    conn = sqlite3.connect('corporate.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY, name TEXT, department TEXT, email TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS documents
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT, category TEXT)''')
    
    c.execute("INSERT OR IGNORE INTO employees VALUES (1, 'John Doe', 'Engineering', 'john@company.com')")
    c.execute("INSERT OR IGNORE INTO employees VALUES (2, 'Jane Smith', 'Sales', 'jane@company.com')")
    c.execute("INSERT OR IGNORE INTO employees VALUES (3, 'Bob Wilson', 'Engineering', 'bob@company.com')")
    
    c.execute("INSERT OR IGNORE INTO documents VALUES (1, 'Q4 Sales Report', 'Sales increased by 20% in Q4 2024...', 'reports')")
    c.execute("INSERT OR IGNORE INTO documents VALUES (2, 'Engineering Guidelines', 'Follow these coding standards...', 'guidelines')")
    c.execute("INSERT OR IGNORE INTO documents VALUES (3, 'HR Policy', 'Employee benefits and policies...', 'hr')")
    
    conn.commit()
    conn.close()

init_sample_db()


@mcp.tool()
def search_documents(query: str) -> str:
    """
    Search corporate documents and knowledge base.
    
    Args:
        query: Search query string
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM documents 
        WHERE title LIKE ? OR content LIKE ? OR category LIKE ?
    """, (f'%{query}%', f'%{query}%', f'%{query}%'))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    if not results:
        return f"No documents found matching '{query}'"
    
    return json.dumps(results, indent=2)

@mcp.tool()
def query_employees(query: str) -> str:
    """
    Search for employee information by name, department, or email.
    
    Args:
        query: Employee name, department, or email to search for
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM employees 
        WHERE name LIKE ? OR department LIKE ? OR email LIKE ?
    """, (f'%{query}%', f'%{query}%', f'%{query}%'))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    if not results:
        return f"No employees found matching '{query}'"
    
    return json.dumps(results, indent=2)


@mcp.tool()
def get_department_stats(department: str) -> str:
    """
    Get statistics for a specific department.
    
    Args:
        department: Department name
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) as employee_count 
        FROM employees 
        WHERE department LIKE ?
    """, (f'%{department}%',))
    
    result = dict(cursor.fetchone())
    conn.close()
    
    return json.dumps({
        "department": department,
        "employee_count": result['employee_count']
    }, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio")