import pandas as pd
import os
import glob
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

def build_chunks_from_csv(csv_path: str) -> list:
    if not os.path.exists(csv_path):
        return []
    df = pd.read_csv(csv_path)
    chunks = []
    # Sample a few rows to avoid massive embedding cost for this demo
    for _, row in df.sample(min(100, len(df))).iterrows():
        # Summarize KPI row into text
        txt = f"On {row['Date']}, product {row['Product']} had sales of {row['Sales']} in the {row['Region']} region. Customer was {row['Customer_Age']} yrs old, {row['Customer_Gender']}, satisfaction {row['Customer_Satisfaction']}."
        chunks.append(txt)
    return chunks

def extract_pdf_chunks(pdf_dir: str, splitter) -> list:
    docs = []
    if not os.path.exists(pdf_dir):
        return docs
    for pdf_file in glob.glob(os.path.join(pdf_dir, "*.pdf")):
        try:
            loader = PyPDFLoader(pdf_file)
            split_docs = loader.load_and_split(splitter)
            docs.extend(split_docs)
        except Exception as e:
            print(f"Skipping {pdf_file}: {e}")
    return docs

def build_vectorstore(csv_path, pdf_dir, persist_path="../data/vectorstore"):
    os.makedirs(os.path.dirname(persist_path), exist_ok=True)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    
    print("Loading CSV Data...")
    csv_chunks = build_chunks_from_csv(csv_path)
    csv_docs = splitter.create_documents(csv_chunks)
    
    print("Loading PDF Documents...")
    pdf_docs = extract_pdf_chunks(pdf_dir, splitter)
    
    all_docs = csv_docs + pdf_docs
    if not all_docs:
        print("No documents found. Please check data directory.")
        return
        
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not found. Skipping embedding generation.")
        return
        
    print(f"Generating embeddings for {len(all_docs)} chunks...")
    embeddings = OpenAIEmbeddings()
    vs = FAISS.from_documents(all_docs, embeddings)
    vs.save_local(persist_path)
    print(f"Vector store built successfully at {persist_path}.")

if __name__ == "__main__":
    build_vectorstore(
        csv_path="../data/sales_data.csv",
        pdf_dir="../data/",
        persist_path="../data/vectorstore"
    )
