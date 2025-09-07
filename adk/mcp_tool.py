from mcp.server.fastmcp import FastMCP
import aiohttp
import traceback

mcp = FastMCP("pokemon_type")

@mcp.tool()
async def get_pokemon_type(pokemon_name: str) -> str:
    """Get a pokemon's type by searching them up using their name

    Args:
        pokemon_name (str): The name of the pokemon whose type we want

    Returns:
        str: The pokemon's type
    """

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}") as resp:
                data = await resp.json()

        return "/".join([type["type"]["name"] for type in data['types']])
    except Exception as e:
        with open("mcp.log", "a") as f:
            f.write(traceback.format_exception(e))

if __name__ == "__main__":
    mcp.run(transport='stdio')