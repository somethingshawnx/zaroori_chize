import os
import chromadb
from chromadb.utils import embedding_functions

class MemoryManager:
    def __init__(self, collection_name="user_context", persist_directory="./chroma_db"):
        """Initializes local ChromaDB for long-term memory."""
        # Initialize the Chroma client with a local directory for persistence
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        
        # Use a lightweight sentence-transformer model for embeddings
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        # Get or create the collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

    def add_context(self, document_id: str, text_content: str, metadata: dict = None):
        """Adds a document (like a resume or rule) to the vector db.
        
        Note: The embedding_function will automatically generate embeddings for the text.
        """
        if metadata is None:
            metadata = {}
            
        metadata["source_id"] = document_id

        self.collection.add(
            documents=[text_content],
            metadatas=[metadata],
            ids=[document_id]
        )
        print(f"Successfully added document ID '{document_id}' to local memory.")

    def search_context(self, query_text: str, n_results: int = 3):
        """Searches the vector db for relevant context based on a text query."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        return results

    def clear_memory(self):
        """Clears all documents from the collection."""
        document_ids = self.collection.get()['ids']
        if document_ids:
            self.collection.delete(ids=document_ids)
            print("Memory cleared.")

if __name__ == "__main__":
    # Test initialization
    try:
        print("Initializing Local ChromaDB Memory Manager...")
        memory = MemoryManager()
        print("Memory Manager initialized successfully.")
    except Exception as e:
        print(f"Initialization failed: {e}")
