# recommend.py
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
# expects a function that takes a 3-row DataFrame -> str
from formatter import format_recommendations

# --- Config ---
INDEX_PATH = "../assets/faiss_index.bin"
EMB_MODEL = "all-MiniLM-L6-v2"
DATA_PATH = "../assets/perfume_data.json"

# --- Load model, index, and data once ---
model = SentenceTransformer(EMB_MODEL)
index = faiss.read_index(INDEX_PATH)
df = pd.read_json(DATA_PATH)

# Columns we want to pass to the formatter
COLUMNS = [
    "Perfume", "Brand", "Country", "Gender", "Rating Value", "Rating Count",
    "Year", "Top", "Middle", "Base", "Perfumer1", "Perfumer2",
    "mainaccord1", "mainaccord2", "mainaccord3", "mainaccord4", "mainaccord5"
]


def get_recommendations(query: str, top_k: int = 3) -> pd.DataFrame:
    """Return the top_k DataFrame rows most similar to the query."""
    q_emb = model.encode([query], normalize_embeddings=True).astype("float32")
    D, I = index.search(q_emb, top_k)
    # If your FAISS index was built with IDs not matching row order, map IDs -> row indices here.
    rows = df.iloc[I[0]].copy()
    # (optional) keep only the columns needed for formatting
    rows = rows[COLUMNS]
    return rows


def recommend_text(query: str, top_k: int = 3) -> str:
    """Return a plain-text formatted answer for the query."""
    rows = get_recommendations(query, top_k=top_k)
    if rows.empty:
        return "No close matches found."
    return format_recommendations(rows)


# if __name__ == "__main__":
#     user_query = input("Describe what you're looking for: ")
#     print(recommend_text(user_query))
