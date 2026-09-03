from google.adk.agents import Agent

from .tools import (
    search_topic,
    calculator,
    request_human_approval
)

from .memory_tools import (
    save_preference,
    get_preference,
    get_all_preferences
)

# --------------------------------------------------
# RESEARCH AGENT
# --------------------------------------------------

research_agent = Agent(
    name="research_agent",
    model="gemini-2.5-flash",
    description="Research specialist",
    instruction="""
    You are a research specialist.

    Your responsibilities:

    - Research topics
    - Explain concepts
    - Summarize information

    Always use search_topic tool when
    external knowledge is needed.
    """,
    tools=[
        search_topic
    ]
)

# --------------------------------------------------
# ANALYTICS AGENT
# --------------------------------------------------

analytics_agent = Agent(
    name="analytics_agent",
    model="gemini-2.5-flash",
    description="Analytics specialist",
    instruction="""
    You are a data and math expert.

    Use calculator tool whenever
    calculations are required.
    """,
    tools=[
        calculator
    ]
)

approval_agent = Agent(
    model="gemini-2.5-flash",
    name="approval_agent",
    description="Handles human approval workflows.",
    instruction="""
    If an action can impact systems, finances, calculation
    deployments or external users,
    request approval before execution.

    Never execute directly.
    """,
    tools=[
        request_human_approval
    ]
)

# --------------------------------------------------
# ROOT COORDINATOR
# --------------------------------------------------

root_agent = Agent(
    name="coordinator_agent",
    model="gemini-2.5-flash",
    description="Main orchestration agent",
    instruction="""
    You coordinate all activities.

    Routing Rules:

    1. Research questions
       -> research_agent

    2. Numerical questions
       -> analytics_agent

    Memory Guidelines:

    If user says:
    - Remember my name
    - Save this preference
    - Store this information

    Use save_preference.

    If user asks:
    - What is my name?
    - What do you remember?
    - Show my preferences

    Use memory tools.

    Always leverage memory before
    asking user for data already stored.
    """,
    tools=[
        save_preference,
        get_preference,
        get_all_preferences
    ],
    sub_agents=[
        research_agent,
        analytics_agent,
        approval_agent
    ]
)