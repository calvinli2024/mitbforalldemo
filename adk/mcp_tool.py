from typing import Any
from mcp.server.fastmcp import FastMCP
import aiohttp
import random

mcp = FastMCP("pokemon_name")

@mcp.tool()
async def get_pokemon() -> str:
    """Get a pokemon

    Returns:
        str: pokemon's name
    """

    try:
        id = random.randint(1, 1025)
        with open("mcp.log", "a") as f:
            f.write(f"ID: {id}")

        response = await aiohttp.request("GET", f"https://pokeapi.co/api/v2/pokemon/{id}")

        data = response.json()

        return data['name']
    except Exception as e:
        with open("mcp.log", "a") as f:
            f.write(e)

if __name__ == "__main__":
    print("Starting Pokemon MCP server")

    mcp.run(transport='stdio')