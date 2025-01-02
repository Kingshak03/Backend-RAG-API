import json, pytest
from app import app
from Appendix import TheAppendix

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_initial_ingest(client):
    for i in TheAppendix:
        response = client.post('/ingest', json={"text": i['text'], "id": i['id']})
        assert response.status_code == 200

        
def test_ingest(client):
    response = client.post('/ingest', json={"text": "Shaker is a great candidate for the Software Engineer Intern position", "id": 8})
    assert response.status_code == 200
    assert b"Text ingested successfully!" in response.data

def test_query(client):
    # Ingest some more data for testing the query
    client.post('/ingest', json={"text": "This is another  test document for querying", "id": 9})

    # Test the query endpoint
    response = client.get('/query', query_string={"text": "Who is the best person for the software engineer intern position?"})
    assert response.status_code == 200
    response_data = json.loads(response.data)
    print(response_data)
    assert "results" in response_data
    
    assert len(response_data["results"]) > 0 # Defined by K, basically how many relevant passages you wanted
    
    assert "text" in response_data["results"][0]
    assert "Shaker" in response_data["results"][0]["text"]
    
    assert "distance" in response_data["results"][0] # Lower the number, the more relevant

