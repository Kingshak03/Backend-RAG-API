# Backend-RAG-API

The Assignment:
Develop a Retrieval-Augmented Generation (RAG) that

- stores documents(text passages),
- converts them into embeddings using sentence-transformers,
- then uses FAISS to search for the most relevant document(s) for a user query.

Install the required Python libraries:
I used a virtual enviornment, so you might want to create and activate it ( )

1. **Create and activate the virtual environment:**

   ```bash
   python3 -m venv myenv

   # Activate
   # On Windows:
   myenv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

Libraries Needed:

sentence-transformers: State-of-the-Art Text Embeddings

FAISS: A library for efficient similarity search and clustering of dense vectors. ([https://faiss.ai/index.html](https://faiss.ai/index.html))

pytest: A simple powerful testing with Python [https://docs.pytest.org/en/stable/](https://docs.pytest.org/en/stable/)

Flask: A simple framework for building complex web applications. [https://flask.palletsprojects.com/en/stable/](https://flask.palletsprojects.com/en/stable/)
