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

# Apparently there's bugs in ADK that cause sub-agents to have a hard time calling tools
# As such, the 'get_pokemon_type' tool will be passed to the parent agent instead
# https://github.com/google/adk-python/issues/53
# https://github.com/google/adk-python/issues/2839

def create_get_pokemon_agent():
    get_pokemon_agent_instruction = """
        Your ONLY responsibility is to return six random pokemon name from your own memory.
        The pokemon can be from any generation, not just the first generation.
        Return only the pokemon names, do not engage in any other tasks or conversations.
        Never return a blank response.
    """

    agent = Agent(
        name="get_pokemon_agent",
        model=llm, 
        description="Retrieves six random pokemon.",
        instruction=get_pokemon_agent_instruction
    )

    print("Created `get_pokemon_agent`")

    return agent

def create_pokemon_team_agent():
    get_pokemon_agent = create_get_pokemon_agent()

    pokemon_team_agent_instruction = """
        Create a team of six pokemon using the 'get_pokemon_agent'.
        You have a specialized sub-agent named 'get_pokemon_agent' that handles choosing pokemon.
        Delegate to the 'get_pokemon_agent' with a request to retrieve six pokemon.
        Once you receive the six pokemon, use the 'get_pokemon_type' tool to retrieve each pokemon's type.
        Analyze the user's request, only answer it if it is a request for constructing a pokemon team. If it's any other request, politely decline.
        Only reply with the final team of six pokemon and their types. Do not include any extra commentary in your response.
        Don't return the following example output, it's just a reference.

        # Example Output
        1. Golbat (Poison)
        2. Pikachu (Electric)
        3. Charizard (Fire/Flying)
        4. Ditto (Normal)
        5. Bulbasaur (Grass)
        6. Caterpie (Bug)
    """
    
    description = """
        The main coordinator agent. 
        Handles building pokemon teams consisting of six pokemon, and delegates pokemon selection to sub agents. 
        Uses the 'get_pokemon_type' tool to get the pokemon type.
    """

    toolset = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command='python',
                args=['mcp_tool.py'],
            ),
        ),
        tool_filter=['get_pokemon_type']
    )

    agent = Agent(
        name="pokemon_team_agent",
        model=llm,
        description=description,
        instruction=pokemon_team_agent_instruction,
        tools=[
            agent_tool.AgentTool(agent=get_pokemon_agent),
            toolset
        ]
    )

    print("Created `pokemon_team_agent`")

    return agent