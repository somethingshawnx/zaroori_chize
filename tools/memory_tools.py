from crewai.tools import BaseTool
import sys
import os

# Add the parent directory to the path so we can import memory_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_manager import MemoryManager

class ContextQueryTool(BaseTool):
    name: str = "Query User Context"
    description: str = "Search the user's long-term memory (like their resume, rules, or past preferences) for relevant information. Provide a search query as input."

    def _run(self, query: str) -> str:
        try:
            memory = MemoryManager()
            # Perform the search
            results = memory.search_context(query)
            
            # The structure of ChromaDB query results is a dictionary
            documents = results.get("documents", [[]])[0]
            if not documents:
                return "No relevant context found in the user's memory."
            
            # Combine the retrieved documents
            context = "\n---\n".join(documents)
            return f"Found the following context from memory:\n{context}"
            
        except Exception as e:
            return f"Error retrieving context from memory: {e}"
