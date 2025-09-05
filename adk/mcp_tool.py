from typing import Any
from mcp.server.fastmcp import FastMCP
from requests import get
import logging

mcp = FastMCP("pokemon_name")

@mcp.tool()
async def get_pokemon_name(id: int) -> str:
    """Retrieve the name of the pokemon with the passed `id`

    Args:
        id (int): ID of pokemon

    Raises:
        Exception: If `id` is not between 1 and 9999, inclusive

    Returns:
        str: pokemon's name
    """
    try:
        if id < 1 or id > 9999:
            raise Exception("ID must be between 1 and 9999, inclusive.")

        response = get(f"https://pokeapi.co/api/v2/pokemon/{id}")

        data = response.json()

        return data['name']
    except Exception as e:
        print(e)
        logging.error(e)

if __name__ == "__main__":
    print("Starting Pokemon MCP server")

    mcp.run(transport='stdio')