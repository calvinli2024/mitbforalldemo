from agents import create_pokemon_team_agent
from runner import run_conversation
import warnings
import logging
import asyncio
from dotenv import load_dotenv

load_dotenv(".env", override=True)

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    pokemon_team_agent = create_pokemon_team_agent()
    
    print("Running conversation")

    pokemon_team = asyncio.run(run_conversation(pokemon_team_agent), debug=True)

    print()
    print(f"Pokemon team: {pokemon_team}")