import os

from dotenv import load_dotenv

# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_qdrant import QdrantVectorStore

load_dotenv()

COLLECTION_NAME = "academic_mentor_multiformat"


def get_embeddings():

    print("Loading Embedding Model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding Model Loaded")

    return embeddings


def create_vector_store(chunks):

    print("\nCreating Qdrant Vector Store...")

    embeddings = get_embeddings()

    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=COLLECTION_NAME,
    )

    print("Embeddings Generated")
    print("Qdrant Collection Created")


def load_vector_store():

    embeddings = get_embeddings()

    db = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=COLLECTION_NAME,
    )

    print("Qdrant Collection Loaded")

    return db