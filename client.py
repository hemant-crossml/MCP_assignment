import os
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
import asyncio


load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY","")


async def main():
    client = MultiServerMCPClient(  
        {
            "math": {
                "transport": "stdio",  # Local subprocess communication
                "command": "python",
                # Absolute path to your math_server.py file
                "args": ["mathserver.py"],
            },
            "weather": {
                "transport": "streamable_http",  # HTTP-based remote server
                # Ensure you start your weather server on port 8000
                "url": "http://localhost:8000/mcp",
            }
        }
    )
    tools =  await client.get_tools() 
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        api_key=gemini_api_key
    ) 
    agent = create_agent(
        model=model,
        tools=tools 
    )
    math_response =  await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    
    print("Maths response:", math_response['messages'][-1].content)

asyncio.run(main())