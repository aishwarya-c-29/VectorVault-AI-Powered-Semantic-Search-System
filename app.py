import faiss
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

from embeddings import get_embedding
from data import documents

app = FastAPI()

# Step 1: Create embeddings
doc_embeddings = get_embedding(documents)

# Step 2: Create FAISS index
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(doc_embeddings))

# Request model
class Query(BaseModel):
    text: str
    top_k: int = 3

# Step 3: Search API
@app.post("/search")
def search(query: Query):
    query_vec = get_embedding([query.text])
    
    distances, indices = index.search(np.array(query_vec), query.top_k)

    results = []
    for i in indices[0]:
        results.append(documents[i])

    return {
        "query": query.text,
        "results": results
    }
