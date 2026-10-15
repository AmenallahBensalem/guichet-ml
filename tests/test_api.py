from fastapi.testclient import TestClient

from app import main
from app.main import app

client = TestClient(app)


def test_health_mode_mock():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["mode"] == "mock"


def test_detection_francais():
    r = client.post("/detect-language",
                    json={"text": "Je ne peux plus acceder a mon compte."})
    assert r.status_code == 200
    assert r.json()["language"] == "fr"


def test_detection_arabe():
    # "Je ne peux pas acceder a mon compte" en arabe, ecrit en codes Unicode
    texte = "\u0644\u0627 \u0623\u0633\u062a\u0637\u064a\u0639 \u0627\u0644\u062f\u062e\u0648\u0644 \u0625\u0644\u0649 \u062d\u0633\u0627\u0628\u064a"
    r = client.post("/detect-language", json={"text": texte})
    assert r.status_code == 200
    assert r.json()["language"] == "ar"



def test_detection_arabe_lisible():
    r = client.post(
        "/detect-language",
        json={"text": "لا أستطيع الدخول إلى حسابي"}
    )
    assert r.status_code == 200
    assert r.json()["language"] == "ar"


def test_texte_trop_court_rejete():
    assert client.post("/detect-language", json={"text": "ab"}).status_code == 422


def test_champ_text_absent_rejete():
    assert client.post("/detect-language", json={}).status_code == 422


def test_fournisseur_en_panne_renvoie_503_sans_secret(monkeypatch):
    def panne(text):
        raise RuntimeError("panne http://interne.local/modele?token=SECRET123")

    monkeypatch.setattr(main.provider, "detect_language", panne)
    r = client.post("/detect-language", json={"text": "Bonjour tout le monde"})
    assert r.status_code == 503
    assert "SECRET123" not in r.text
    assert "interne.local" not in r.text