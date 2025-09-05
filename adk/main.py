from agents import create_pokemon_name_agent, create_pokemon_team_agent
from runner import run_conversation
import warnings
import logging
import asyncio
from dotenv import load_dotenv

load_dotenv(".env", override=True)

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

if __name__ == "__main__":
    pokemon_name_agent = create_pokemon_name_agent()

    print()
    print("Created `pokemon_name_agent`")

    pokemon_team_agent = create_pokemon_team_agent(pokemon_name_agent)
    
    print()
    print("Created `pokemon_team_agent`")
    
    print()
    print("Running conversation")

    pokemon_team = asyncio.run(run_conversation(pokemon_team_agent))

    print()
    print(f"Pokemon team: {pokemon_team}")