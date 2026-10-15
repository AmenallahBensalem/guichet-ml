# guichet-ml

API FastAPI de détection de langue, avec fournisseur simulé (mock) et fournisseur Hugging Face.

## Installation (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

## Lancer l'API

```powershell
uvicorn app.main:app --reload
```

Puis ouvrir http://127.0.0.1:8000/docs

## Tests

```powershell
python -m pytest -q
```

## Configuration

Voir `.env.example`. Le mode par défaut est `INFERENCE_MODE=mock` (aucun jeton nécessaire).
Ne jamais versionner `.env`.