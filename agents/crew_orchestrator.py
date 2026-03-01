from crewai import Crew, Process, Task
from agents.task_agent import create_task_agent
from agents.research_agent import create_research_agent

class ProductivityCrew:
    def __init__(self):
        self.task_agent = create_task_agent()
        self.research_agent = create_research_agent()

    def process_request(self, user_request: str) -> str:
        """Determines what the user wants and orchestrates the agents."""
        
        # We define dynamic tasks based on the general user request
        # Note: In a more complex system, an "Orchestrator Agent" might decide which tasks to create.
        # For simplicity and speed (free tier limits), we define the tasks directly based on the request.
        
        # 1. Research Task (if the request implies needing information)
        research_task = Task(
            description=f"Analyze this request and find any necessary information: '{user_request}'. If no research is needed, simply summarize the core concept.",
            expected_output="A summary of research findings relevant to the user's request, or a statement that no external research is required.",
            agent=self.research_agent
        )

        # 2. Planning/Action Task
        planning_task = Task(
            description=f"Based on the original request ('{user_request}') and the research findings, formulate a clear, prioritized action plan or response.",
            expected_output="A structured markdown response addressing the user's needs, complete with next steps, synthesized information, or a prioritized to-do list.",
            agent=self.task_agent,
            context=[research_task] # This task waits for the research task to finish to use its output
        )

        # Create the Crew
        crew = Crew(
            agents=[self.research_agent, self.task_agent],
            tasks=[research_task, planning_task],
            process=Process.sequential, # Execute strictly in order
            verbose=True
        )

        # Start the execution
        result = crew.kickoff()
        return str(result)
