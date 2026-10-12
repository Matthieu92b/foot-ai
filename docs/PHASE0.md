# Phase 0 — Checklist (≈ 1 semaine)

## 1. Repo (jour 1)
- [✅] Créer le repo GitHub (privé au début, public au lancement)
- [✅] Pousser ce squelette sur `main`
- [✅] `./scripts/setup_labels.sh`
- [✅] Protéger `main` : PR obligatoire, 1 review, CI verte (Settings → Branches / Rulesets)
- [✅] Remplacer `@TON_PSEUDO` dans `.github/CODEOWNERS`
- [✅] Créer un GitHub Project (Kanban) : Backlog · Planifié · En cours · Review · Done
- [✅] Copier le PDF roadmap dans `docs/`

## 2. Agents GitHub (jour 2)
- [✅] Installer l'app Claude GitHub sur le repo (ou `/install-github-app` depuis Claude Code)
- [✅] Ajouter le secret `ANTHROPIC_API_KEY` (ou `CLAUDE_CODE_OAUTH_TOKEN` + modifier les workflows)
- [✅] Test Dev : issue « ajouter un test pour track.py » → commenter `@claude …` → une PR doit apparaître
- [✅] Test Reviewer : la PR reçoit une revue automatique

## 3. n8n (jour 3)
- [ ] `cd infra/n8n && cp .env.example .env && docker compose up -d`
- [ ] Créer les credentials (GitHub, Claude, Discord)
- [ ] Construire le workflow Planner (voir `docs/n8n-planner.md`) et l'exporter dans `infra/n8n/workflows/`
- [ ] Test de bout en bout : idée → plan → `@claude go` → PR → review → merge

## 4. Données (jours 4-6)
- [ ] Filmer / récupérer 5 à 10 vidéos de five (téléphone fixe, en hauteur, accord des joueurs)
- [ ] Lancer `ml/scripts/track.py` sur 2-3 clips → noter les problèmes observés (issues !)
- [ ] Annoter ~200 images (Roboflow ou CVAT) : joueur, gardien, arbitre, ballon
- [ ] Récupérer les datasets publics Roboflow (joueurs, ballon, points clés)

## 5. Veille (jour 7)
- [ ] Chercher l'existant « five / small-sided » sur GitHub, Hugging Face, Product Hunt
- [ ] Mettre à jour la section positionnement si besoin

## ✅ Phase 0 terminée quand
Repo protégé + flux d'agents testé de bout en bout + dataset d'évaluation prêt.
