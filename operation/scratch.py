# https://www.datacamp.com/tutorial/deepseek-r1-rag

import numpy

import ollama
import re
import gradio as gr
from concurrent.futures import ThreadPoolExecutor
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from chromadb.config import Settings
from chromadb import Client
from langchain.vectorstores import Chroma



from langchain.docstore.document import Document as LC_Document

from database import model, init_db
import basetypes as bt

session = init_db(
    'dataset.csv',
    'sqlite:////tmp/my.db'
)

emails = session.query(model.Message).all()


emails = bt.randomly_split_iter(emails, .05)[0]

# Convert each database record into a LangChain Document

documents = []
for record in emails:
    content = (
        f"This message is {"spam" if record.spam else "ham"}."
        f"Subject: {record.subject}"
        f"{record.body}"
    )
    documents.append(
        LC_Document(page_content=content, metadata={"id": record.id})
    )



# from langchain.text_splitter import RecursiveCharacterTextSplitter
#
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# chunks = text_splitter.split_documents(documents)

# chunks = documents
chunks = [LC_Document(page_content="booboo", metadata={"id": 0})]

embedding_function = OllamaEmbeddings(model="deepseek-r1")

def generate_embedding(chunk):
    return embedding_function.embed_query(chunk.page_content)

with ThreadPoolExecutor() as executor:
    embeddings = list(executor.map(generate_embedding, chunks))

# bt.pickle_it(embeddings, "embed")




from chromadb.config import Settings
from chromadb import Client

client = Client(Settings())
# client.delete_collection(name="documents_collection")  # Remove existing collection if needed
collection = client.create_collection(name="documents_collection")

for idx, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk.page_content],
        metadatas=[{'id': chunk.metadata.get("id")}],
        embeddings=[embeddings[idx]],
        ids=[str(idx)]  # IDs as strings
    )