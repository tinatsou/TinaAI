"""
Simple RAG example using LlamaIndex.

This script demonstrates how to load local documents, build a vector index,
and query it. It supports choosing between OpenAI and local LLMs (via Ollama),
and between default, Chroma, or Pinecone vector stores.

Usage:
    python rag_quickstart.py --data_dir=path_to_documents \
        --llm_type=openai --vector_store=chroma \
        --question="Your question"
"""

import os
import argparse
from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext
from llama_index.vector_stores import ChromaVectorStore, PineconeVectorStore
from llama_index.storage import StorageContext
from llama_index.llms import OpenAI  # default LLM
# If using a local LLM, import Ollama at runtime.

def build_index(data_dir: str, llm_type: str = "openai",
                vector_store_type: str = "default"):
    # Load documents
    documents = SimpleDirectoryReader(input_dir=data_dir).load_data()

    # Select the LLM
    if llm_type == "openai":
        # Requires OPENAI_API_KEY env var
        llm = OpenAI(temperature=0.0, model="gpt-3.5-turbo")
    elif llm_type == "local":
        from llama_index.llms import Ollama
        llm = Ollama(model="llama2")
    else:
        raise ValueError(f"Unsupported llm_type: {llm_type}")

    service_context = ServiceContext.from_defaults(llm=llm)

    # Configure the vector store
    if vector_store_type == "chroma":
        from chromadb import PersistentClient
        client = PersistentClient(path="./chroma_db")
        vector_store = ChromaVectorStore(
            chroma_client=client, collection_name="rag_quickstart")
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
    elif vector_store_type == "pinecone":
        import pinecone
        api_key = os.getenv("PINECONE_API_KEY")
        env = os.getenv("PINECONE_ENVIRONMENT")
        if not api_key or not env:
            raise RuntimeError("Pinecone API key and environment must be set.")
        pinecone.init(api_key=api_key, environment=env)
        index_name = "rag-quickstart-index"
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(index_name, dimension=1536)
        pinecone_index = pinecone.Index(index_name)
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
    else:
        # default in-memory vector store
        storage_context = StorageContext.from_defaults()

    return VectorStoreIndex.from_documents(
        documents,
        service_context=service_context,
        storage_context=storage_context,
    )

def query_index(index: VectorStoreIndex, question: str):
    query_engine = index.as_query_engine()
    return query_engine.query(question)

def main():
    parser = argparse.ArgumentParser(
        description="RAG Quickstart example using LlamaIndex.")
    parser.add_argument("--data_dir", default="data",
                        help="Directory containing documents to index.")
    parser.add_argument("--llm_type", choices=["openai", "local"],
                        default="openai")
    parser.add_argument("--vector_store",
                        choices=["default", "chroma", "pinecone"],
                        default="default")
    parser.add_argument("--question",
                        default="What is this project about?",
                        help="Question to ask the index.")
    args = parser.parse_args()

    index = build_index(args.data_dir,
                        llm_type=args.llm_type,
                        vector_store_type=args.vector_store)
    response = query_index(index, args.question)
    print(response)

if __name__ == "__main__":
    main()
