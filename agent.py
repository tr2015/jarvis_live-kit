import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RoomInputOptions
from livekit.plugins import google, noise_cancellation

from prompt import AGENT_INSTRUCTION, SESSION_INSTRUCTION

load_dotenv()


class Jarvis(Agent):
    def __init__(self):
        super().__init__(
            instructions=AGENT_INSTRUCTION,
                llm=google.beta.realtime.RealtimeModel(
                voice="Aoede",
                temperature=0.7,
            ),
        )


async def entrypoint(ctx: agents.JobContext):
    print("Starting Jarvis...")

    session = AgentSession()

    await session.start(
        room=ctx.room,
        agent=Jarvis(),
        room_input_options=RoomInputOptions(
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()
    
    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint
        )
    )