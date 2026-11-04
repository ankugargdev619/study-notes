import asyncio
from picoagents import Agent
from picoagents.llm import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from picoagents.orchestration import RoundRobinOrchestrator
from picoagents.termination import MaxMessageTermination, TextMentionTermination
from picoagents.webui import serve

load_dotenv()

# Setup the language model client
client = OpenAIChatCompletionClient(
    model="gpt-4.1-mini", api_key=os.getenv("OPENAI_API_KEY")
)

poet = Agent(
    name="poet",
    description="Haiku poet.",
    instructions="You are a Haiku poet.",
    model_client=client,
)


async def test_poet():
    response = await poet.run("Write a haiku aboutt cherry blossoms in spring")
    print(f"Poet says: {response}")


critic = Agent(
    name="critic",
    description="Poetry critic who provides constructive feedback on haikus.",
    instructions="You are a haiku critic. \
        When you see a haiku, provide 2-3 specific, actionable \
        suggestions for improvement. Be constructive and brief. \
        If satisfied with the haiku, respond with 'APPROVED'",
    model_client=client,
)


async def test_critic():
    haiku = (
        "Cherry blossoms fall\nPetals dancing in spring breeze\nNature's gentle song"
    )
    response = await critic.run(f"Please critique this haiku: {haiku}")
    print(f"Critic says: {response}")


termination = MaxMessageTermination(max_messages=8) | TextMentionTermination(
    text="APPROVED"
)

orchestrator = RoundRobinOrchestrator(
    agents=[poet, critic], termination=termination, max_iterations=4
)


async def run_orchestration():
    task = "Write a haiku about cherry blossoms in spring"
    stream = orchestrator.run_stream(task)
    async for message in stream:
        print(f"{message}")


serve(entities=[orchestrator], port=8070, auto_open=True)

# asyncio.run(run_orchestration())
