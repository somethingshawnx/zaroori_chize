from crewai import Agent
from tools.google_tools import CalendarReadTool

def create_calendar_agent():
    return Agent(
        role='Schedule Manager',
        goal='Monitor the user calendar for upcoming events and ensure they are prepared for the day.',
        backstory="""You are a meticulous scheduler. You analyze the user's upcoming calendar events, 
        identify potential conflicts, and provide a clear, prioritized overview of their day. 
        You help the user stay ahead of their commitments.""",
        verbose=True,
        allow_delegation=False,
        tools=[CalendarReadTool()]
    )
