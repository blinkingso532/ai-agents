"""_summary_"""

import os
import shutil
import tempfile

from src.rag_app.ingest import ingest
from src.rag_app.vectorstore import VectorStore


def test_ingest_and_query():
    """_summary_"""

    tmpdir = tempfile.mkdtemp()
    data_dir = os.path.join(tmpdir, "data")
    os.makedirs(data_dir, exist_ok=True)
    sample_path = os.path.join(data_dir, "sample.txt")
    with open(sample_path, "w", encoding="utf-8") as f:
        f.write(
            "This is a test document about FastAPI and embeddings.\nIt contains useful information."
        )
    index_dir = os.path.join(tmpdir, "index")
    ingest(data_dir=data_dir, index_dir=index_dir)
    vs = VectorStore()
    index, docs = vs.load_index(index_dir)
    results = vs.query("What is FastAPI?", index, docs, top_k=2)
    assert len(results) >= 1
    shutil.rmtree(tmpdir)
