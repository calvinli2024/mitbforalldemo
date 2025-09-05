from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
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

def create_pokemon_name_agent():
    pokemon_name_agent_instruction = """
    You are a helpful pokemon search agent. 
    When the user asks for a pokemon, pick a random number from 1 to 9999 (inclusive),
    and use the `get_pokemon_name` tool to get the pokemon's name.
    If the tool has an error, politely tell the user 'Tool encountered error'.
    If the tool was successful, return the pokemon name directly.
    """

    return Agent(
        name="pokemon_name_agent",
        model=llm, 
        description="Retrieves a random pokemon for the user using the `get_pokemon_name` tool",
        instruction=pokemon_name_agent_instruction,
        tools=[
            MCPToolset(
                connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command='python',
                        args=['mcp_tool.py'],
                    ),
                ),
                tool_filter=['get_pokemon_name']
            )
        ]
    )

def create_pokemon_team_agent(pokemon_name_agent: Agent):
    pokemon_team_agent_instruction = """
    You are the main agent responsible for building pokemon teams. 
    Your sole responsibility is to create a team of six pokemon.
    You have a specialized sub-agent named 'pokemon_name_agent', that handles retrieving a pokemon. Delegate to it whenever you need a pokemon.
    You must use the 'pokemon_name_agent' sub agent to retrieve pokemon names, don't use your own memory.
    Analyze the user's request, only answer it if it is a request for constructing a pokemon team. If it's any other request, politely decline.
    """

    return Agent(
        name="pokemon_team_agent",
        model=llm,
        description="The main coordinator agent. Handles building pokemon teams consisting of six pokemon, and delegates pokemon selection to child agents.",
        instruction=pokemon_team_agent_instruction,
        sub_agents=[pokemon_name_agent]
    )