# Multi-Agent Patterns
The multi agent systems can be classified broadly into 2 type of patterns
## Workflow Patterns
These patterns provide developer-defined execution paths with predictable behavior. A common emergent practice is to borrow concepts from graph theory and model multi-agent orchestration as computational graphs where nodes represent computational units and edges control flow between nodes.
> Node : A unit within a graph, these have defined inputs which they can process and generate an output data structure.
> Edge : A connection between nodes that defines control flow  or transitions between two nodes. If an edge is connecting node A with node B then the edge would represent that the output of node A is converted into input of node B.

There are following type of the workflow patterns
### Sequential Workflows
In this pattern the agents are run in a sequence, consider agent A and B are running in sequence. This means that the agent B will only start running after the agent A execution is completed and there is a given contract between agent A and B which allows output of agent A to be passed into agent B.

flowchart LR
    A([User Input]) --> B[Orchestrator]
    B --> C[Research]
    C --> D[Strategy]
    D --> E[Content]
    E --> F[Design]
    F --> G[Review]
    G --> H{Approved?}
    H -->|Yes| I([Final Output])
    H -->|No| E

### Conditional Workflows
Conditional workflows are orchestration patterns that use logic-based edges to determine the next node which needs to be executed. This pattern extends naturally to supervisor-style workflows, a conditional workflow variant where a central node evaluates request and routes tasks to specialized agents based on task characteristics.
flowchart LR
    A([User Input]) --> B[Orchestrator]
    B --> C{Intent Detection}

    C -->|Research| D[Research Agent]
    C -->|Content| E[Content Agent]
    C -->|Support| F[Support Agent]

    D --> G[Result Validator]
    E --> G
    F --> G

    G --> H{Valid?}
    H -->|Yes| I([Final Output])
    H -->|No| J[Error Handler]
    J --> B

### Parallel Workflows
Parallel workflows are the patterns that enable concurrent execution of independent tasks using Direct Acyclic Graphs (DAGs), with fan-out phases that split work and fan-in phases that combine results. These patterns are useful where the work can be parallelised without any side effects.
flowchart LR
    A([User Input]) --> B[Orchestrator]

    B --> C1[Research Agent]
    B --> C2[Content Agent]
    B --> C3[Analysis Agent]

    C1 --> D[Aggregator]
    C2 --> D
    C3 --> D

    D --> E[Review Agent]
    E --> F([Final Output])

## Autonomous Patterns


