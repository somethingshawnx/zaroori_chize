from crewai import Crew, Process, Task
from agents.task_agent import create_task_agent
from agents.research_agent import create_research_agent
from agents.email_agent import create_email_agent
from agents.calendar_agent import create_calendar_agent
from agents.executive_agent import create_executive_agent

class ProductivityCrew:
    def __init__(self):
        # Original Agents
        self.task_agent = create_task_agent()
        self.research_agent = create_research_agent()
        
        # New Specialized Agents
        self.email_agent = create_email_agent()
        self.calendar_agent = create_calendar_agent()
        self.executive_agent = create_executive_agent()

    def process_request(self, user_request: str) -> str:
        """Determines what the user wants and orchestrates the agents."""
        
        # If the user is specifically asking for a "Daily Briefing" or similar
        if "briefing" in user_request.lower() or "day" in user_request.lower():
            return self._run_daily_briefing(user_request)
        
        # Otherwise, fall back to the generic research -> plan flow
        research_task = Task(
            description=f"Analyze this request and find any necessary information: '{user_request}'. If no research is needed, simply summarize the core concept.",
            expected_output="A summary of research findings relevant to the user's request.",
            agent=self.research_agent
        )

        planning_task = Task(
            description=f"Based on the original request ('{user_request}') and the research findings, formulate a clear, prioritized action plan or response.",
            expected_output="A structured markdown response addressing the user's needs.",
            agent=self.task_agent,
            context=[research_task]
        )

        crew = Crew(
            agents=[self.research_agent, self.task_agent],
            tasks=[research_task, planning_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)
        
    def _run_daily_briefing(self, user_request: str) -> str:
        """A specialized workflow for generating a comprehensive daily summary."""
        
        calendar_task = Task(
            description="Fetch the upcoming events from the user's calendar.",
            expected_output="A clear list of upcoming scheduled events and times.",
            agent=self.calendar_agent
        )
        
        email_task = Task(
            description="Fetch the unread emails from the user's Gmail inbox.",
            expected_output="A summarized list of important unread emails.",
            agent=self.email_agent
        )
        
        executive_task = Task(
            description=f"""Create a comprehensive daily briefing for the user based on their calendar, emails, and any specific requests they made ({user_request}). 
            Crucially, YOU MUST use your ContextQueryTool to search the user's long-term memory for their resume or context (use queries like 'John Doe' or 'user background' or 'resume'). 
            Tailor the tone and the priorities in the briefing based on the context you find.""",
            expected_output="A beautifully formatted markdown Daily Briefing, referencing the user's specific context/resume, calendar schedule, and email summaries.",
            agent=self.executive_agent,
            context=[calendar_task, email_task]
        )
        
        crew = Crew(
            agents=[self.calendar_agent, self.email_agent, self.executive_agent],
            tasks=[calendar_task, email_task, executive_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)
