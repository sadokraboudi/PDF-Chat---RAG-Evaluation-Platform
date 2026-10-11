from app.chat.embeddings.gemini import embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os 

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    # environment=os.getenv("PINECONE_ENV_Name")  old code 
)

index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings,
)

def build_retriever(chat_args , k):
    search_kwargs = {
        "filter": { "pdf_id": chat_args.pdf_id},
        "k": k
             }
    return vector_store.as_retriever(
        search_kwargs = search_kwargs
    )