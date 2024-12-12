import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_milvus import Milvus
from pymilvus import MilvusClient


def milvus():
    return Milvus(embedding_function=embedding(), collection_name=st.secrets["collection_name"], connection_args={"uri": st.secrets["milvus_uri"], "token": st.secrets["milvus_token"]}, auto_id=True)


def embedding():
    return GoogleGenerativeAIEmbeddings(model=f"models/{st.secrets['embedded']}", google_api_key=st.secrets["api_key"])


def pdf_extractor(path):
    pages = []
    for page in PyPDFLoader(file_path=path).load():
        pages.append(page)
    return pages

def csv_extractor(path):
    loader = CSVLoader(file_path=path, encoding="utf-8")
    data = loader.load()
    return data

def add_pdf(byte_file):
    vector_db = milvus()
    with open(byte_file.name, mode="wb") as w:
        w.write(byte_file.getvalue())
    vector_db.add_documents(documents=pdf_extractor(byte_file.name))

def add_csv(byte_file):
    vector_db = milvus()
    with open(byte_file.name, mode="wb") as w:
        w.write(byte_file.getvalue())    
    vector_db.add_documents(documents=csv_extractor(byte_file.name))


def available_document():
    client = MilvusClient(uri=st.secrets["milvus_uri"], token=st.secrets["milvus_token"])
    try:
        results = client.query(collection_name=st.secrets["collection_name"], filter="pk > 0", output_fields=["source"])
    except:
        results = []
    unique_sources = set()
    for result in results:
        source = result.get("source", None)
        unique_sources.add(source)
    return list(unique_sources)