from google.adk.sessions import InMemorySessionService
from google.adk.runners import InMemoryRunner, Runner
from google.genai import types
from google.adk.agents import Agent
from dotenv import load_dotenv
import os

load_dotenv(".env", override=True)

async def call_agent_async(
    query: str, 
    runner: Runner, 
    user_id: str, 
    session_id: str
) -> str:
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent didn't send final response."

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.

    debug = os.environ.get("DEBUG", 'false') == 'true'
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if debug:
            print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent error: {event.error_message or 'No specific message.'}"

            break

    if debug:
        print(f"Pokemon team: {final_response_text}")

    return final_response_text

async def run_conversation(pokemon_team_agent: Agent):
    session_service = InMemorySessionService()

    app_name = "pokemon_team_builder"
    user_id = "pokemon_team_builder_user"
    session_id = "session_1_pokemon_team_builder"

    session = await session_service.create_session(
        app_name=app_name, 
        user_id=user_id, 
        session_id=session_id
    )

    runner_agent_team = Runner(
        agent=pokemon_team_agent,
        app_name=app_name,
        session_service=session_service
    )

    return await call_agent_async(
        query = "Build a team of six pokemon for me.",
        runner=runner_agent_team,
        user_id=user_id,
        session_id=session_id
    )