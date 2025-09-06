from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import agent_tool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import warnings
import logging

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

load_dotenv('.env', override=True)

#Ollama server running in background
llm = LiteLlm(model="openai/qwen3:8b")

def create_get_pokemon_agent():
    get_pokemon_agent_instruction = """
    Your ONLY responsibility is to return six random pokemon name from your own memory.
    Return only the pokemon names, do not engage in any other tasks or conversations.
    Never return a blank response.
    """

    # Apparently there's a bug where sub-agents in ADK have a hard time calling tools
    # https://github.com/google/adk-python/issues/53

    def get_pokemon() -> str:
        """Get a pokemon

        Returns:
            str: pokemon's name
        """

        return "Steelix"

    agent = Agent(
        name="get_pokemon_agent",
        model=llm, 
        description="Retrieves six random pokemon.",
        instruction=get_pokemon_agent_instruction
    )

    # MCPToolset(
    #     connection_params=StdioConnectionParams(
    #         server_params=StdioServerParameters(
    #             command='python',
    #             args=['mcp_tool.py'],
    #         ),
    #     ),
    #     tool_filter=['get_pokemon']
    # )

    print("Created `get_pokemon_agent`")

    return agent

def create_pokemon_team_agent():
    get_pokemon_agent = create_get_pokemon_agent()

    pokemon_team_agent_instruction = """ 
    Create a team of six pokemon using the 'get_pokemon_agent'.
    You have a specialized sub-agent named 'get_pokemon_agent' that handles choosing pokemon. 
    Delegate to the 'get_pokemon_agent' with a request to retrieve six pokemon.
    Analyze the user's request, only answer it if it is a request for constructing a pokemon team. If it's any other request, politely decline.
    Only reply with the final team of six pokemon. Do not include any extra commentary in your response.
    Don't return the following example output, it's just a reference.

    # Example Output
    1. Golbat
    2. Pikachu
    3. Charizard
    4. Ditto
    5. Bulbasaur
    6. Caterpie
    """
    
    agent = Agent(
        name="pokemon_team_agent",
        model=llm,
        description="The main coordinator agent. Handles building pokemon teams consisting of six pokemon, and delegates pokemon selection to sub agents.",
        instruction=pokemon_team_agent_instruction,
        tools=[
            agent_tool.AgentTool(agent=get_pokemon_agent)
        ]
    )

    print("Created `pokemon_team_agent`")

    return agent