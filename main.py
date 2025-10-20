import os
import time
import base64
from datetime import datetime
import fitz  # PyMuPDF
from openai import OpenAI
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.schema import Document as LangchainDocument
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- 1. SETUP & INITIALIZATION ---

# Load environment variables from .env file
load_dotenv()

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Initialize OpenAI client for guardrails and vision
client = OpenAI()

# Global variables for the RAG components
ensemble_retriever = None
RETRIEVAL_LOG = []

# --- 2. HELPER FUNCTIONS ---

def normalize_text(text):
    """Normalizes text by lowercasing and removing extra whitespace."""
    return " ".join(text.lower().split())

def summarize_image(image_bytes, image_filename, page_num):
    """Uses GPT-4o to summarize an image and returns a LangchainDocument."""
    try:
        b64_image = base64.b64encode(image_bytes).decode('utf-8')
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "Describe this image in detail. If it's a chart or graph, explain its findings."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                ]}
            ],
            max_tokens=1024,
        )
        summary = response.choices[0].message.content
        metadata = {
            "source": image_filename, "page": page_num, "type": "image_summary",
            "ingestion_timestamp": time.time()
        }
        return LangchainDocument(page_content=summary, metadata=metadata)
    except Exception as e:
        print(f"-> Error summarizing image on page {page_num} of {image_filename}: {e}")
        return None

# --- 3. CORE RAG LOGIC ---

def process_documents(directory_path):
    """Processes all documents in a directory for multi-modal RAG."""
    docs = []
    print(f"-> Starting document processing in '{directory_path}'...")
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if not filename.lower().endswith(".pdf"):
            print(f"   - Skipping non-PDF file: {filename}")
            continue
        try:
            doc = fitz.open(file_path)
            print(f"   - Processing PDF: {filename}")
            for page_num, page in enumerate(doc, start=1):
                # Extract text
                text = page.get_text()
                if text:
                    metadata = {"source": filename, "page": page_num, "type": "text", "ingestion_timestamp": time.time()}
                    docs.append(LangchainDocument(page_content=normalize_text(text), metadata=metadata))
                # Extract tables
                for table in page.find_tables():
                    table_text = f"Table on page {page_num}:\n{table.to_pandas().to_string()}"
                    metadata = {"source": filename, "page": page_num, "type": "table", "ingestion_timestamp": time.time()}
                    docs.append(LangchainDocument(page_content=normalize_text(table_text), metadata=metadata))
                # Extract and summarize images
                for img_index, img in enumerate(page.get_images(full=True)):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_doc = summarize_image(image_bytes, filename, page_num)
                    if image_doc:
                        docs.append(image_doc)
        except Exception as e:
            print(f"-> Error processing PDF {filename}: {e}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    print(f"--> Split {len(docs)} source elements into {len(chunks)} chunks.")
    return chunks

def build_retriever(chunks):
    """Builds and returns a hybrid retriever."""
    CHROMA_PATH = "rag_cli_db"
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH)
    
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 5
    vector_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    
    retriever = EnsembleRetriever(retrievers=[bm25_retriever, vector_retriever], weights=[0.5, 0.5])
    print("--> Hybrid retriever built successfully.")
    return retriever

def check_guardrails(text):
    """Checks for harmful content using OpenAI's moderation endpoint."""
    response = client.moderations.create(input=text)
    return not response.results[0].flagged

def log_retrieval(query, docs):
    """Logs retrieval events."""
    log_entry = {
        "timestamp": datetime.now().isoformat(), "query": query,
        "retrieved_sources": [doc.metadata for doc in docs]
    }
    RETRIEVAL_LOG.append(log_entry)

# --- 4. MAIN EXECUTION ---

def main():
    """Main function to run the RAG CLI application."""
    print("--- Advanced Multi-Modal RAG CLI ---")
    
    # Ingestion
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created '{data_dir}' directory. Please add your PDF documents there and restart.")
        return
        
    chunks = process_documents(data_dir)
    if not chunks:
        print("No documents were processed. Please check the 'data' directory.")
        return
        
    retriever = build_retriever(chunks)
    
    # RAG Chain Definition
    prompt_template = """
    Answer the question based only on the context provided. For each piece of information, cite the source file and page number in brackets, like .
    Context: {context}\nQuestion: {question}
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Command-Line Interface Loop
    while True:
        print("\n" + "="*50)
        query = input("Enter your question (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        
        # Guardrail check on input
        if not check_guardrails(query):
            print("Your query was flagged as inappropriate. Please rephrase.")
            continue

        # Generation Path
        print("\n-> Generating answer...")
        answer = rag_chain.invoke(query)
        
        # Guardrail check on output
        if not check_guardrails(answer):
            answer = "[Generated response was flagged as inappropriate and has been redacted.]"

        # Retrieve sources for citation
        retrieved_docs = retriever.invoke(query)
        log_retrieval(query, retrieved_docs)

        print(f"\n🤖 Answer:\n{answer}")
        
        # Format and print sources
        print("\n--- 📚 Sources Used ---")
        unique_sources = set()
        for doc in retrieved_docs:
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', 'N/A')
            content_type = doc.metadata.get('type', 'content').capitalize()
            unique_sources.add(f"- {source} (Page: {page}, Type: {content_type})")
        
        for source_citation in sorted(list(unique_sources)):
            print(source_citation)

if __name__ == "__main__":
    main()
