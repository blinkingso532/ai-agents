import os
import pickle
from typing import List, Tuple

try:
    import faiss
except Exception:
    faiss = None

from sentence_transformers import SentenceTransformer
import numpy as np


class VectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        return np.array(self.model.encode(texts, convert_to_numpy=True))

    def build_index(self, texts: List[str], index_dir: str):
        os.makedirs(index_dir, exist_ok=True)
        embeddings = self.embed_documents(texts)
        dim = embeddings.shape[1]
        if faiss is None:
            raise RuntimeError("faiss is required. Install faiss-cpu package.")
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        faiss.write_index(index, os.path.join(index_dir, "index.faiss"))
        with open(os.path.join(index_dir, "docs.pkl"), "wb") as f:
            pickle.dump(texts, f)

    def load_index(self, index_dir: str) -> Tuple[object, List[str]]:
        if faiss is None:
            raise RuntimeError("faiss is required. Install faiss-cpu package.")
        index = faiss.read_index(os.path.join(index_dir, "index.faiss"))
        with open(os.path.join(index_dir, "docs.pkl"), "rb") as f:
            docs = pickle.load(f)
        return index, docs

    def query(
        self, question: str, index, docs: List[str], top_k: int = 4
    ) -> List[Tuple[float, str]]:
        q_emb = self.model.encode([question], convert_to_numpy=True)
        D, I = index.search(q_emb, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            results.append((float(dist), docs[int(idx)]))
        return results
