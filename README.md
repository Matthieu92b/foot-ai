# ⚽ Foot AI — Analyste vidéo IA pour le foot amateur

> Filmer un match au téléphone → suivi des joueurs, vue tactique 2D, stats, assistant IA.

🚧 **Statut : phase 0 (cadrage & outillage)**

| Dossier | Contenu |
|---|---|
| `ml/` | Vision : détection, tracking, équipes, homographie |
| `ai/` | Service IA : agent, text-to-SQL, RAG |
| `backend/` | API Spring Boot |
| `frontend/` | App Angular |
| `infra/` | Docker Compose, n8n |
| `docs/` | Roadmap, état de l'art, prompts des agents |

Démarrage rapide (baseline tracking) :
```bash
pip install -r ml/requirements.txt
python ml/scripts/track.py --source match.mp4
```

Développement : voir [AGENTS.md](AGENTS.md) et [docs/PHASE0.md](docs/PHASE0.md).
