from langchain.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@tool
def multiply(a: int, b: int)->int:
    """Multiply two numbers"""
    return a*b

@tool
async def get_weather(Location : str)->str:
    """Get the weather location"""
    return "It's always raining in California"