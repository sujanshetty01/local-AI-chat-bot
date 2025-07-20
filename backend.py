from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import tempfile
import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker
import uuid

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite setup
DATABASE_URL = "sqlite:///./uploads.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

uploads_table = Table(
    "uploads",
    metadata,
    Column("id", String, primary_key=True),
    Column("filename", String),
)
metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# In-memory store for vector DB and retriever (per upload)
vector_dbs = {}
retrievers = {}

class QueryRequest(BaseModel):
    question: str
    upload_id: str

@app.post("/upload_csv/")
def upload_csv(file: UploadFile = File(...)):
    # Save uploaded file to temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name
    # Load CSV
    df = pd.read_csv(tmp_path)
    os.unlink(tmp_path)
    # Store in SQLite
    upload_id = str(uuid.uuid4())
    df.to_sql(upload_id, engine, if_exists="replace", index=False)
    # Register upload in uploads table
    db = SessionLocal()
    db.execute(uploads_table.insert().values(id=upload_id, filename=file.filename))
    db.commit()
    db.close()
    # Convert rows to text
    texts = df.astype(str).apply(lambda row: ', '.join(row), axis=1).tolist()
    # Split text if needed
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = splitter.create_documents(texts)
    # Embedding model
    embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # Create vector DB
    vector_db = FAISS.from_documents(docs, embedder)
    retriever = vector_db.as_retriever()
    vector_dbs[upload_id] = vector_db
    retrievers[upload_id] = retriever
    return {"status": "CSV uploaded and embedded", "upload_id": upload_id}

@app.post("/query/")
def query_csv(req: QueryRequest):
    retriever = retrievers.get(req.upload_id)
    if retriever is None:
        return {"error": "No CSV uploaded yet or invalid upload_id."}
    # Use Ollama LLM via LangChain
    llm = Ollama(model="gemma3")
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    answer = qa.run(req.question)
    return {"answer": answer}

@app.post("/reset_db/")
def reset_db():
    # Drop all CSV tables (but not uploads table)
    insp = inspect(engine)
    with engine.connect() as conn:
        for table_name in insp.get_table_names():
            if table_name != "uploads":
                conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        # Clear uploads table
        conn.execute(uploads_table.delete())
    return {"status": "Database reset successful"} 