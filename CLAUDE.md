# CLAUDE.md — Règles du projet pour Claude Code

## Projet
Analyste vidéo IA pour le foot amateur : vidéo de match → tracking → vue 2D → stats → assistant IA.
MVP : foot à 5, caméra fixe. Voir `docs/roadmap.pdf` et `AGENTS.md`.

## Structure
- `ml/` Python 3.11 — vision (YOLO, tracking, homographie). `ml/core/` = cœur ML, **ne pas modifier sans demande explicite**.
- `ai/` Python — service FastAPI (agent, text-to-SQL, RAG).
- `backend/` Java 21 / Spring Boot 3 — API métier.
- `frontend/` Angular 18 — UI.
- `infra/` Docker Compose, n8n.

## Conventions
- Branches : `claude/<num-issue>-<slug>` pour les agents, `feat/...` / `fix/...` pour Matthieu.
- Commits : Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`, `chore:`).
- Python : ruff (lint + format), type hints, pytest. Java : tests JUnit 5. Angular : standalone components, signals.
- Une PR = une issue. Lier l'issue avec `Closes #N`. Rester sous ~400 lignes modifiées.
- Toujours ajouter ou mettre à jour les tests du code modifié.

## Interdits
- Pousser sur `main`, modifier `.github/workflows/` sans demande, committer des secrets, vidéos ou poids de modèles (`data/`, `*.pt`).
- Inventer des métriques ou résultats.

## Langue
Code et noms en anglais ; commentaires de PR, docs et échanges en français.
