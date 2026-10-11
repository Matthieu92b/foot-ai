# Workflow n8n — Agent Planner

GitHub ne peut pas appeler un n8n qui tourne en local. Deux options :
- **Polling (recommandé pour commencer)** : n8n vérifie les issues toutes les 5 min. Rien à exposer.
- **Webhook** : exposer n8n (Cloudflare Tunnel / ngrok) et utiliser le nœud *GitHub Trigger*. Plus réactif, à faire plus tard.

## Nœuds (version polling)

| # | Nœud n8n | Réglage |
|---|---|---|
| 1 | **Schedule Trigger** | Toutes les 5 minutes |
| 2 | **GitHub** → Issue → Get Many | Repo du projet, `state = open`, `labels = idée` |
| 3 | **Filter** | Garder les issues dont `labels` ne contient pas `planifié` |
| 4 | **HTTP Request** → Claude API | `POST https://api.anthropic.com/v1/messages` · headers `x-api-key`, `anthropic-version: 2023-06-01`, `content-type: application/json` · body : `model` = `claude-sonnet-5-5`, `max_tokens` = 2000, `system` = contenu de `docs/prompts/planner.md`, `messages` = `[{role: "user", content: "Titre : {{title}}\n\n{{body}}"}]` |
| 5 | **GitHub** → Issue → Create Comment | Texte : `{{ $json.content[0].text }}` |
| 6 | **HTTP Request** → GitHub | `POST /repos/{owner}/{repo}/issues/{number}/labels` · body `{"labels": ["planifié"]}` (ajoute sans écraser) |
| 7 | **Discord** (Webhook) | « 🧠 Plan prêt pour #{{number}} — {{title}} » |

## Credentials à créer dans n8n
- **GitHub** : token *fine-grained* limité au repo (Issues : read/write).
- **Header Auth** pour Claude : `x-api-key` = ta clé API.
- **Discord** : URL de webhook du salon `#foot-ai`.

## Test
1. Crée une issue avec le template « Idée » (label `idée` auto).
2. Attends ≤ 5 min → commentaire du Planner + label `planifié` + notif Discord.
3. Réponds `@claude go …` → l'agent Dev (GitHub Action) prend le relais.
