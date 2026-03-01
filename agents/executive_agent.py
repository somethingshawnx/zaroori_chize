from crewai import Agent
from tools.memory_tools import ContextQueryTool

def create_executive_agent():
    return Agent(
        role='Executive Assistant',
        goal='Synthesize information from emails and calendars, consult user context, and create a comprehensive daily briefing and action plan.',
        backstory="""You are the ultimate Executive Assistant. You understand your user deeply. 
        You take the raw data provided by the Email and Calendar agents, retrieve relevant context 
        from the user's long-term memory, and generate a personalized, highly actionable daily summary.""",
        verbose=True,
        allow_delegation=True, # The Executive can delegate tasks to other agents
        tools=[ContextQueryTool()]
    )
