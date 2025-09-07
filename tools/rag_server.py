from fastmcp import FastMCP
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

mcp = FastMCP("FAQ_RAG")

# Load data
DATA = Path("../data/faq_data.csv")
df = pd.read_csv(DATA)

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode(df["question"].tolist(), convert_to_numpy=True, normalize_embeddings=True)
d = embeddings.shape[1]
index = faiss.IndexFlatIP(d)
index.add(np.array(embeddings, dtype="float32"))

# ✅ Core function
def search_faq_core(q: str, k: int = 1):
    q_vec = model.encode([q], convert_to_numpy=True, normalize_embeddings=True).astype("float32")
    D, I = index.search(q_vec, k)
    results = []
    for score, idx in zip(D[0].tolist(), I[0].tolist()):
        results.append({
            "question": str(df.iloc[idx]["question"]),
            "answer": str(df.iloc[idx]["answer"]),
            "score": float(score)
        })
    return {"results": results}

# MCP tool wrapper
@mcp.tool()
def search_faq(q: str, k: int = 1) -> dict:
    return search_faq_core(q, k)

if __name__ == "__main__":
    mcp.run()
