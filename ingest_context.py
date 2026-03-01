import os
import argparse
from pypdf import PdfReader
import docx
from memory_manager import MemoryManager

def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def read_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.txt':
        return read_text(file_path)
    elif ext == '.pdf':
        return read_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        return read_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Supported formats: .txt, .pdf, .docx")

def main():
    parser = argparse.ArgumentParser(description="Ingest documents into the local ChromaDB long-term memory.")
    parser.add_argument("file_path", help="Path to the document (e.g., resume.pdf, context.txt)")
    parser.add_argument("--doc_id", help="Optional ID for the document. If not provided, filename is used.", default=None)
    parser.add_argument("--clear", action="store_true", help="Clear existing memory before ingesting new document.")
    
    args = parser.parse_args()
    
    # 1. Provide an easy default ID if the user didn't give one
    doc_id = args.doc_id if args.doc_id else os.path.basename(args.file_path)
    
    print(f"Reading file: {args.file_path}...")
    try:
        text_content = extract_text_from_file(args.file_path)
        print(f"Extraction successful. Length: {len(text_content)} characters.")
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 2. Add to ChromaDB
    print("Connecting to Local ChromaDB...")
    memory = MemoryManager()
    
    if args.clear:
        memory.clear_memory()
        
    print(f"Ingesting into ChromaDB with ID '{doc_id}'...")
    memory.add_context(
        document_id=doc_id, 
        text_content=text_content, 
        metadata={"source": args.file_path, "type": "user_context"}
    )
    
    print("\n✅ Ingestion complete! The agents can now retrieve this context.")

if __name__ == "__main__":
    main()
