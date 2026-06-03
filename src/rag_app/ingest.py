import argparse
import os
from typing import List

from .vectorstore import VectorStore


def load_texts(data_dir: str) -> List[str]:
    texts = []
    for fn in sorted(os.listdir(data_dir)):
        path = os.path.join(data_dir, fn)
        if os.path.isfile(path) and path.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                texts.append(f.read())
    return texts


def chunk_text(text: str, max_chars: int = 1000) -> List[str]:
    if len(text) <= max_chars:
        return [text]
    parts = []
    start = 0
    while start < len(text):
        parts.append(text[start : start + max_chars])
        start += max_chars
    return parts


def ingest(data_dir: str, index_dir: str, model_name: str = "all-MiniLM-L6-v2"):
    texts = load_texts(data_dir)
    chunks = []
    for t in texts:
        chunks.extend(chunk_text(t))
    vs = VectorStore(model_name=model_name)
    vs.build_index(chunks, index_dir)
    print(f"Indexed {len(chunks)} chunks into {index_dir}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="data")
    parser.add_argument("--index_dir", default="index")
    parser.add_argument("--model", default="all-MiniLM-L6-v2")
    args = parser.parse_args()
    ingest(args.data_dir, args.index_dir, args.model)


if __name__ == "__main__":
    main()
