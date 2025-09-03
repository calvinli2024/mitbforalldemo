from agents import create_pokemon_agent, create_pokemon_team_agent
from runner import run_conversation
import warnings
import logging

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

if __name__ == "__main__":
    pokemon_agent = create_pokemon_agent()

    print()
    print("Created `pokemon_agent`")

    pokemon_team_agent = create_pokemon_team_agent(pokemon_agent)
    
    print()
    print("Created `pokemon_team_agent`")
    
    print()
    print("Running conversation")

    pokemon_team = run_conversation(pokemon_team_agent)

    print()
    print(f"Pokemon team: {pokemon_team}")