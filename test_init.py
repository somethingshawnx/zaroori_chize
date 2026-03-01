from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = "dummy_key_to_bypass_crewai_validation"

import traceback

try:
    print("Initializing Crew...")
    from agents.crew_orchestrator import ProductivityCrew
    crew = ProductivityCrew()
    print("Successfully Initialized Crew!")
except Exception as e:
    print("FAILED TO INITIALIZE CREW:")
    print(repr(e))
    traceback.print_exc()
