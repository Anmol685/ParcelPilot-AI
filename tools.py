import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# Current project path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def search_documents(query):

    # PDF folder
    pdf_folder = os.path.join(BASE_DIR, "data", "pdfs")

    documents = []

    # Load all PDFs
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_folder, file))
            documents.extend(loader.load())

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    # Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)
    
    # Create Vector DB
    db = FAISS.from_documents(chunks, embeddings)

    # Search
    results = db.similarity_search(query, k=3)

    context = ""

    for doc in results:
        context += doc.page_content + "\n\n"

    return context