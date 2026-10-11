#!/usr/bin/env bash
# Crée les labels du projet (nécessite GitHub CLI : gh auth login)
set -euo pipefail
create() { gh label create "$1" --color "$2" --description "$3" --force; }
create "idée"      "C5DEF5" "Idée brute, à planifier"
create "planifié"  "0E8A16" "Plan rédigé par le Planner"
create "en-cours"  "FBCA04" "En développement"
create "bloqué"    "B60205" "Bloqué / question ouverte"
create "bug"       "D73A4A" "Bug"
create "ml"        "5319E7" "Vision / ML"
create "ai"        "1D76DB" "Service IA"
create "backend"   "0052CC" "Spring Boot"
create "frontend"  "006B75" "Angular"
create "ui"        "F9D0C4" "Design / UI"
create "infra"     "BFDADC" "Docker, CI, n8n"
create "tests"     "E4E669" "Tests"
create "docs"      "D4C5F9" "Documentation"
for i in 0 1 2 3 4 5 6 7 8; do create "phase-$i" "EDEDED" "Phase $i de la roadmap"; done
echo "Labels OK"
