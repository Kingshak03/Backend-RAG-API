from flask import Flask, request, jsonify, Response
from sentence_transformers import SentenceTransformer
import faiss
from Appendix import TheAppendix
app = Flask(__name__)


# To convert texts into embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/
index = faiss.IndexFlatL2(384) # all-MiniLM-L6-v2 uses 384 dimensional vectors

document_store = {}

# POST /ingest – Ingest new text to be stored in the vector store.
@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_json()
    
    text = data.get("text")
    doc_id = data.get("id")
    
    if not text or not doc_id:
        response = Response(response="Missing 'text' or 'id' in request body", status=400)
        return response
    
    if doc_id in document_store:
        response = Response(response="Document with id already exists!", status=400)
        return response
    
    # Embedd the given passages
    embeddings = model.encode([text])
    
    # Store both the raw passage and its embedding in your chosen vector store
    index.add(embeddings)
    document_store[doc_id] = text

    response = Response(response="Text ingested successfully!", status=200)
    return response

# GET /query?text=... – Retrieve the most relevant ingested text(s) for a user’s text
@app.route('/query', methods=['GET'])
def query():
    user_query = request.args.get("text")
    
    if not user_query:
        response = Response(response="Missing 'text' in query parameters", status=400)
        return response
    
    # Embedd the query text
    query_embedding = model.encode([user_query])
    
    # https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/
    # Search for the 2 most relevant passages
    D, I = index.search(query_embedding, k=2)
    results = []
    
    list_of_keys = list(document_store.keys())
    for idx, distance in zip(I[0], D[0]):
        if idx != -1:
            doc_id = list_of_keys[idx]
            # print("SHAKER!! " + str(list(document_store.keys())[idx]) + " First: " + str(idx))
            text = document_store[doc_id]
            results.append({"id": doc_id, "text": text, "distance": float(distance)})
    
    return jsonify({"results": results}), 200