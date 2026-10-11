# AGENTS.md — Équipe d'agents du projet

Chaque tâche part d'une **issue GitHub** et traverse la chaîne ci-dessous.
Deux validations humaines sont obligatoires : **le plan** et **le merge**.

```
Issue (label idée) → Planner → ✋ "@claude go" → Dev → PR → CI → Reviewer (+ Designer si UI) → ✋ merge → Doc → n8n (Done + notif)
```

| Agent | Version | Déclencheur | Entrées | Sorties | Droits | Garde-fous |
|---|---|---|---|---|---|---|
| **Planner** | V1 | Issue avec label `idée` (`claude-planner.yml`) | Titre + description de l'issue | Commentaire : user story, critères d'acceptation, sous-tâches, estimation, risques. Label `planifié` | Commenter, poser des labels | Ne code jamais. Pose des questions si le ticket est flou |
| **Dev** | V1 | Commentaire `@claude` sur une issue/PR (`claude.yml`) | Issue + plan du Planner + `CLAUDE.md` | Branche `claude/...` + PR liée à l'issue | Pousse sur sa branche uniquement | Jamais sur `main`. Ne modifie pas `ml/core/` sauf demande explicite. PR < ~400 lignes |
| **Reviewer** | V1 | PR ouverte/mise à jour (`claude-review.yml`) | Diff + issue liée | Commentaires inline ou résumé | Lecture + commentaires | Ne modifie pas le code |
| **Tester** | V2 (phase 3) | CI en échec / label `tests` | Logs CI + diff | Tests ajoutés ou diagnostic | Pousse sur la branche de la PR | N'efface jamais un test existant pour faire passer la CI |
| **Designer** | V2 (phase 2-3) | Issue label `ui` / PR touchant `frontend/` | `docs/design-system.md` + captures Playwright | Maquette (HTML/image) en commentaire, revue visuelle | Commentaires + fichiers dans `docs/mockups/` | Ne touche pas au code de prod. Respecte la DA définie par Matthieu |
| **Doc** | V2 (phase 3) | Merge sur `main` | Diff mergé | README / CHANGELOG à jour (PR) | PR doc uniquement | Jamais de push direct |
| **Reporter** | V3 (phase 5) | Cron hebdo + fin de phase (n8n) | Issues fermées, PR, métriques MLflow | Bilan hebdo Discord, brouillon de post LinkedIn | Lecture seule | Les chiffres viennent des données, jamais inventés |

## Labels
`idée` · `planifié` · `en-cours` · `ui` · `ml` · `backend` · `frontend` · `infra` · `tests` · `bloqué` · `phase-0` … `phase-8`

## Règles communes
- Le **cœur ML** (`ml/core/` : détection, tracking, homographie, modèles) est développé par Matthieu. Les agents peuvent proposer, pas implémenter seuls.
- Toute affirmation chiffrée (métrique, perf) doit venir d'un run réel (MLflow / CI).
- En cas de doute : poser une question en commentaire plutôt que deviner.
