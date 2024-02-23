from pathlib import Path
import qdrant_client
from llama_index.core import (   
    VectorStoreIndex, 
    ServiceContext, 
    SimpleDirectoryReader, 
    StorageContext
)

# reference: https://docs.llamaindex.ai/en/stable/examples/llm/ollama.html
from llama_index.legacy.llms import Ollama
from llama_index.legacy.vector_stores import QdrantVectorStore

# Loading the documents from the disk
documents = SimpleDirectoryReader("./data").load_data()

# Initializing the vector store with Qdrant
client = qdrant_client.QdrantClient(path="./qdrant_data")
vector_store = QdrantVectorStore(client=client, collection_name="springboot")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Initializing the Large Language Model (LLM) with Ollama
# The request_timeout may need to be adjusted depending on the system's performance capabilities
llm = Ollama(model="llama2", request_timeout=120.0)
service_context = ServiceContext.from_defaults(llm=llm, embed_model="local")

# Creating the index, which includes embedding the documents into the vector store
index = VectorStoreIndex.from_documents(documents, service_context=service_context, storage_context=storage_context)

# Querying the index with a specific question
query_engine = index.as_query_engine()
prompt = (
  "Create a REST controller class in Java for a Spring Boot 3.2 application. "
  "This class should handle GET and POST requests, and include security and "
  "configuration annotations."
)
response = query_engine.query(prompt)
print(response)