#!/bin/bash
# deploy.sh — Pousse tout le corpus vers GitHub
# Usage : bash deploy.sh <GITHUB_PAT>
# Ton PAT doit avoir le scope 'repo' (classic) ou 'contents:write' (fine-grained)

set -e

PAT="${1}"
REPO="crowleycoofficial-ops/AGI-Lux-Ferox"

if [ -z "$PAT" ]; then
  echo "Usage: bash deploy.sh <GITHUB_PAT>"
  echo "Génère un token sur : https://github.com/settings/tokens"
  exit 1
fi

echo "⚒ Lux Ferox — Déploiement GitHub"
echo "Repo : $REPO"
echo ""

# Configure git avec le token
git remote set-url origin "https://${PAT}@github.com/${REPO}.git"
git config user.email "crowleycoofficial@gmail.com"
git config user.name "François Mathieu / Lux Ferox"

# Add all new files
git add .
git status --short

echo ""
read -p "Commit et push ? [o/N] " confirm
if [[ "$confirm" != "o" && "$confirm" != "O" ]]; then
  echo "Annulé."
  exit 0
fi

git commit -m "forge: corpus Zenodo L0-L4 intégré — structure 5 couches + épistémique

- Arborescence docs/L{0,1,2,3,4}_* créée
- ZENODO_INDEX.md : 16 publications 2025-2026, mapping couche + statut épistémique
- README.md : 5 couches remplacent le marketing, équation centrale W_min = k_B T ln2 · S_total
- docs/index.html : carte de forge interactive (GitHub Pages)
- docs/L*/README.md : étiquetage MESURÉ / ESTIMÉ / STRUCTUREL / SPÉCULATIF
- sync_zenodo.py : synchronisation PDF Zenodo → GitHub (renseigner les record_id)
- CITATION.cff : ORCID 0009-0004-1848-870X, v4.0.0

Parole de forgeron — de gré ou de force."

git push origin main

echo ""
echo "✓ Déployé."
echo ""
echo "Pour activer GitHub Pages :"
echo "  → Settings > Pages > Source : Deploy from branch > main > /docs"
echo "  → URL : https://crowleycoofficial-ops.github.io/AGI-Lux-Ferox/"
