from picoagents.orchestration import RoundRobinOrchestrator
from picoagents.termination import MaxMessageTermination, TextMentionTermination

termination = MaxMessageTermination(max_messages=8) | TextMentionTermination(
    text="APPROVED"
)

orchestrator = RoundRobinOrchestrator(
    agents=[poet, critic], termination=termination, max_iterations=4
)
