import os
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from .vectorstore import VectorStore

app = FastAPI(title="RAG MVP")


class QueryRequest(BaseModel):
    question: str
    k: int = 4


@app.on_event("startup")
def startup():
    global VS, INDEX, DOCS
    model_name = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    index_dir = os.environ.get("INDEX_DIR", "index")
    VS = VectorStore(model_name=model_name)
    INDEX, DOCS = VS.load_index(index_dir)


def synthesize_answer(question: str, contexts: List[str]) -> str:
    # Simple synthesizer: concatenate contexts and echo question
    content = "\n---\n".join(contexts)
    return f"Question: {question}\n\nContexts:\n{content}\n\nAnswer (synthesized): Use the above contexts to answer the question."


@app.post("/query")
def query(req: QueryRequest):
    global VS, INDEX, DOCS
    results = VS.query(req.question, INDEX, DOCS, top_k=req.k)
    contexts = [r[1] for r in results]
    answer = synthesize_answer(req.question, contexts)
    return {"answer": answer, "results": results}
