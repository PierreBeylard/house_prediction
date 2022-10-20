from fastapi.testclient import TestClient
import codecs
import pytest

try :
    from .main import app
    from .enrichissement import ExternalApiCalls
except :
    from main import app
    from enrichissement import ExternalApiCalls

client = TestClient(app)

## lancer en amont uvicorn et postgres depuis la racine du programme
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_read_property():
    response = client.get("/property")
    assert response.status_code == 200

def test_read_property_predict():
    response = client.post("/property",
                           data={
                                  "nom": "boulet",
                                  "prenom": "aupier",
                                  "email": "aupier.boulet@hotmail.fr",
                                  "addresse": "32 rue turenne",
                                  "complement": "",
                                  "lieu": "France Metropolitaine",
                                  "commune": "Bordeaux",
                                  "code_postal": "33000",
                                  "nb_pieces_principales": 2,
                                  "surface_reelle_bati": 50,
                                  "surface_terrain": 60,
                                  "Dependance": False,
                                  "type": "Maison",
                                  "neuf": "Neuf",
                                  "terrain": "Jardin"
                           })
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/html; charset=utf-8'


def test_external_api_call():
    df, nb_mutation = ExternalApiCalls(
        "42 rue turenne", "", "France Metropolitaine", "Bordeaux", "33000",
        5, 100, 120, True, "Jardin").call_api_addresse().call_api_pyris()
    assert df["code_postal"][0] == "33000"
