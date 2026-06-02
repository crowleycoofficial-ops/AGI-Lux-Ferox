# AGI Lux Ferox

**Thermodynamic Information Engine · TRL 3 → 4**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)]()
[![Zenodo corpus](https://img.shields.io/badge/Zenodo-16%20publications-blue)](ZENODO_INDEX.md)

> *Lux Ferox Independent Research — artisan practitioner methodology, institutionally unconstrained.*
> *Infrastructure : Chromebook · Google Colab free tier · Zenodo · GitHub · Zero institutional funding.*

---

## Équation centrale

$$W_{\min} = k_B \, T \ln 2 \cdot S_{\text{total}} \qquad \text{où} \qquad S_{\text{total}} = D_{KL}(P_{\text{model}} \| P_{\text{obs}})$$

Landauer bound : coût physique minimal pour résoudre un écart informationnel entre modèle et observation.

---

## Architecture en 5 couches

```
L0  Substrat holographique / gravité quantique
    ├── Quantum Holographic Framework (UAP, Schwinger pair production)
    ├── Janusian Quantum Topology (logique paraconsistante ↔ torsion Einstein-Cartan)
    └── JQTM Kernel (dualité M⁺/M⁻, spin foam–MERA)

L1  Thermodynamique de l'observateur
    ├── TCUS — champ de densité de compétence, liberté asymptotique
    ├── Theory of Limit States (TLS) — égrégores comme objets physiques
    └── Formal Analysis of AI Architectures (limites bayésiennes, Red Queen)

L2  Hardware neuromorphique souverain
    ├── Sentinel Module — OCC, Red Noise Egregore Radar, format HDF5 JANUS-CB
    └── Green Fireballs → Topological Plasma — BCI-MHD, PI-VAE, ASIC neuromorphique
        Stack hardware : CEA-Leti (28nm FDSOI) · Imec (7nm SoC) · X-FAB (180nm)

L3  Boucles réflexives / guerre cognitive
    ├── CognitiveWar v2.9 — HWE, RI, θ, p^state_manip, D_cogbias, τ_inst
    ├── LEGACY Manifesto + LEGACY Program v65 — JQTM, Observer's Cost Theorem
    └── Satoichi Paradox — Bitcoin comme anomalie informationnelle

L4  Instances live / renseignement
    ├── AARO 2024 — AP framework appliqué aux contradictions institutionnelles
    ├── Orbital DEW — HEL/HPM, Shinobi Protocol, vulnérabilités Sentinel/Copernicus
    ├── Metric G — audit Benford/Dempster-Shafer flux DoD/ACF
    └── PURSUE Initiative — analyse CognitiveWar v2.8, RI, θ, MISREP
```

→ Corpus complet des 16 publications : **[ZENODO_INDEX.md](ZENODO_INDEX.md)**
→ Carte interactive des 5 couches : **[docs/index.html](docs/index.html)**

---

## Installation

```bash
git clone https://github.com/crowleycoofficial-ops/AGI-Lux-Ferox.git
cd AGI-Lux-Ferox
pip install numpy scipy
# Pour synchroniser les PDF Zenodo :
pip install requests
python sync_zenodo.py
```

---

## Usage — Noyau logiciel

### Total Surprise (L1)

```python
import numpy as np
from core import calculate_surprise

p_model = np.array([0.7, 0.2, 0.1])  # prior : croyance du modèle
p_obs   = np.array([0.1, 0.3, 0.6])  # observation empirique

result = calculate_surprise(p_model, p_observed=p_obs, temperature=300.0)

print(f"S_total :  {result['S_total']:.4f} bits")   # D_KL
print(f"W_min   :  {result['W_min_joules']:.4e} J") # Landauer bound à 300K
```

### Physical Constraint Guard (L2)

```python
from core import HardScienceGuardian

guardian = HardScienceGuardian(threshold_load=0.85, sampling_hz=1000.0)

decision = guardian.process_signal(compute_load=0.91, arrival_hz=120.0)
print(decision.action)  # THROTTLE

aliased = guardian.process_signal(compute_load=0.40, arrival_hz=750.0)
print(aliased.action)   # DISCARD  ← dépasse enveloppe Nyquist-Shannon
```

### Consent-Based Promotion Agent (L3 — boucle OODA)

```python
from datetime import datetime, timezone
from core import (AudienceSegment, CampaignBrief, ConsentReceipt,
                  FeedbackEvent, PromotionAgent)

agent = PromotionAgent(
    author_id="author-001",
    allowed_channels=("mastodon", "linkedin"),
    max_posts_per_channel_per_day=2,
)
receipt = ConsentReceipt(
    receipt_id="button-accept-001",
    subject_id="subscriber-001",
    scope="promotion",
    accepted_at=datetime(2026, 6, 2, tzinfo=timezone.utc),
)
segment = AudienceSegment(
    name="research subscribers",
    interest="KLD/Landauer observability",
    consent_basis="owned newsletter opt-in",
    consent_receipt=receipt,
)
brief = CampaignBrief(
    title="AGI-Lux-Ferox",
    objective="share a thermodynamic information-engine update",
    project_url="https://github.com/crowleycoofficial-ops/AGI-Lux-Ferox",
)
plan = agent.generate_plan(
    brief, [segment], ["mastodon"],
    start_at=datetime(2026, 6, 2, tzinfo=timezone.utc),
)
print(plan[0].approval_state)
```

---

## Étiquetage épistémique

Chaque dossier `docs/L*/README.md` porte l'étiquette de statut épistémique :

| Label | Définition |
|-------|-----------|
| **MESURÉ** | Données empiriques ou calculs vérifiables (`core/*.py`, stats Benford, instabilités QuTiP) |
| **ESTIMÉ** | Modélisation avec incertitude quantifiée (simulations, analyses bayésiennes) |
| **STRUCTUREL** | Formalisation théorique sans validation empirique directe (JQTM, TLS, TCUS) |
| **SPÉCULATIF** | Hypothèses heuristiques, extrapolations non falsifiées (NHI, eschatologie computationnelle) |

---

## Tests

```bash
python core/surprise.py
```

---

## Méthode

Synthetic peer-review — direction humaine + collaboration adversariale multi-LLM (DeepSeek, Kimi, Grok, Claude) sous étiquetage épistémique explicite. Pas de peer review institutionnel. Pas de validation externe. Seulement : mesure, estimation, structure, spéculation.

*François Mathieu — Lux Ferox Independent Research — Lyon, France*
*ORCID : 0009-0004-1848-870X*
