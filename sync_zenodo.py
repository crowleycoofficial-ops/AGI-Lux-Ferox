#!/usr/bin/env python3
"""
sync_zenodo.py — Synchronisation corpus Zenodo → GitHub /docs

Usage:
    python sync_zenodo.py [--dry-run]

Télécharge les 16 PDF Zenodo et les place dans l'arborescence L0-L4.
Requires: requests (pip install requests)

Parole de forgeron — de gré ou de force.
"""

import os
import sys
import time
import argparse
import hashlib
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install requests : pip install requests")
    sys.exit(1)

# ─── Mapping complet Zenodo → arborescence GitHub ───────────────────────────
# Format : (record_id_ou_DOI, target_path, label_epistemique)
# Pour les record_id : https://zenodo.org/records/{record_id}
# Remplace XXXXXXX par le vrai record ID Zenodo si nécessaire

CORPUS = [
    # L0 — Substrat holographique
    {
        "title":   "Quantum Holographic Framework (Schwinger → gravitational signatures)",
        "date":    "2025-12-09",
        "version": "v1",
        "doi":     None,  # à renseigner : 10.5281/zenodo.XXXXXXX
        "record":  None,  # à renseigner : ID numérique Zenodo
        "target":  "docs/L0_physics/2025-12-09_quantum-holographic.pdf",
        "layer":   "L0",
        "epi":     "STRUCTUREL / SPÉCULATIF",
    },
    {
        "title":   "Janusian Quantum Topology (paraconsistent framework)",
        "date":    "2026-01-05",
        "version": "v1",
        "doi":     None,
        "record":  None,
        "target":  "docs/L0_physics/2026-01-05_janus.pdf",
        "layer":   "L0",
        "epi":     "STRUCTUREL",
    },
    {
        "title":   "QHF Computational Challenges & Numerical Instabilities",
        "date":    "2026-01-07",
        "version": "v1",
        "doi":     None,
        "record":  None,
        "target":  "docs/L0_physics/2026-01-07_qhf-computational.pdf",
        "layer":   "L0",
        "epi":     "MESURÉ",
    },
    # L1 — Thermodynamique
    {
        "title":   "TCUS — Unified Field Theory of Sovereign Systems",
        "date":    "2025-11-28",
        "version": "v1",
        "doi":     None,
        "record":  None,
        "target":  "docs/L1_thermo/2025-11-28_tcus.pdf",
        "layer":   "L1",
        "epi":     "STRUCTUREL",
    },
    {
        "title":   "Theory of Limit States (TLS) — Semantic Physics & Egregore Engineering",
        "date":    "2026-01-03",
        "version": "v1",
        "doi":     None,
        "record":  None,
        "target":  "docs/L1_thermo/2026-01-03_tls.pdf",
        "layer":   "L1",
        "epi":     "STRUCTUREL / SPÉCULATIF",
    },
    {
        "title":   "Formal Analysis of AI Architectures (Bayesian → Fractal Topology)",
        "date":    "2025-12-29",
        "version": "v1",
        "doi":     None,
        "record":  None,
        "target":  "docs/L1_thermo/2025-12-29_formal-ai.pdf",
        "layer":   "L1",
        "epi":     "STRUCTUREL",
    },
    # L2 — Hardware souverain
    {
        "title":   "Sentinel Module — OCC Framework for Sovereign AGI",
        "date":    "2025-12-25",
        "version": "v1",
        "doi":     None,
        "record":  None,
        "target":  "docs/L2_hardware/2025-12-25_sentinel.pdf",
        "layer":   "L2",
        "epi":     "MESURÉ / ESTIMÉ",
    },
    {
        "title":   "Green Fireballs → Topological Plasma Control (BCI-MHD)",
        "date":    "2026-05-25",
        "version": "v2",
        "doi":     None,
        "record":  None,
        "target":  "docs/L2_hardware/2026-05-25_green-fireballs.pdf",
        "layer":   "L2",
        "epi":     "ESTIMÉ / STRUCTUREL",
    },
    # L3 — Guerre cognitive
    {
        "title":   "LEGACY Program v65 (JQTM + Looking Glass Algorithm)",
        "date":    "2026-05-14",
        "version": "v65",
        "doi":     None,
        "record":  None,
        "target":  "docs/L3_cognitive/2026-05-14_legacy-v65.pdf",
        "layer":   "L3",
        "epi":     "STRUCTUREL / SPÉCULATIF",
    },
    {
        "title":   "LEGACY MANIFESTO (KingSlayer Event & NWOS)",
        "date":    "2026-01-12",
        "version": "v2",
        "doi":     None,
        "record":  None,
        "target":  "docs/L3_cognitive/2026-01-12_manifesto.pdf",
        "layer":   "L3",
        "epi":     "SPÉCULATIF",
    },
    {
        "title":   "Satoichi Paradox — Bitcoin Anomaly via AP Framework",
        "date":    "2026-01-05",
        "version": "v1",
        "doi":     None,
        "record":  None,
        "target":  "docs/L3_cognitive/2026-01-05_satoichi.pdf",
        "layer":   "L3",
        "epi":     "STRUCTUREL / SPÉCULATIF",
    },
    # L4 — Live / Renseignement
    {
        "title":   "PURSUE Initiative — CognitiveWar v2.8 Analysis",
        "date":    "2026-05-30",
        "version": "v1",
        "doi":     "10.5281/zenodo.19021444",
        "record":  "19021444",
        "target":  "docs/L4_live/2026-05-30_pursue.pdf",
        "layer":   "L4",
        "epi":     "MESURÉ",
    },
    {
        "title":   "AARO 2024 Report — Institutional Paradoxicality",
        "date":    "2026-01-04",
        "version": "v1",
        "doi":     None,
        "record":  None,
        "target":  "docs/L4_live/2026-01-04_aaro.pdf",
        "layer":   "L4",
        "epi":     "MESURÉ",
    },
    {
        "title":   "Orbital DEW — Feasibility & Asymmetric Supply Chain",
        "date":    "2026-01-09",
        "version": "v1",
        "doi":     None,
        "record":  None,
        "target":  "docs/L4_live/2026-01-09_dew.pdf",
        "layer":   "L4",
        "epi":     "ESTIMÉ / STRUCTUREL",
    },
    {
        "title":   "Metric G — Federal Budget Efficiency Anomalies",
        "date":    "2026-01-02",
        "version": "v1",
        "doi":     None,
        "record":  None,
        "target":  "docs/L4_live/2026-01-02_metric-g.pdf",
        "layer":   "L4",
        "epi":     "MESURÉ",
    },
    # META
    {
        "title":   "Holographic-Thermodynamic Ontology of Information v28",
        "date":    "2026-05-23",
        "version": "v28",
        "doi":     None,
        "record":  None,
        "target":  "docs/2026-05-23_ontology-v28.pdf",
        "layer":   "META",
        "epi":     "STRUCTUREL",
    },
]


def zenodo_url(record_id: str) -> str:
    """Construit l'URL de téléchargement Zenodo à partir du record ID."""
    api = f"https://zenodo.org/api/records/{record_id}"
    try:
        r = requests.get(api, timeout=15)
        r.raise_for_status()
        data = r.json()
        files = data.get("files", [])
        pdf_files = [f for f in files if f.get("key", "").endswith(".pdf")]
        if pdf_files:
            return pdf_files[0]["links"]["self"]
        # fallback : premier fichier
        if files:
            return files[0]["links"]["self"]
    except Exception as e:
        print(f"  ⚠ Impossible de résoudre l'URL pour record {record_id}: {e}")
    return None


def download_pdf(url: str, target: Path, dry_run: bool = False) -> bool:
    """Télécharge un PDF et le sauvegarde à target."""
    if dry_run:
        print(f"  [DRY-RUN] téléchargerait : {url}")
        print(f"            → {target}")
        return True

    print(f"  ↓ {url}")
    try:
        r = requests.get(url, timeout=60, stream=True)
        r.raise_for_status()
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        size = target.stat().st_size
        print(f"  ✓ {target} ({size // 1024} KB)")
        return True
    except Exception as e:
        print(f"  ✗ Erreur : {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Sync Zenodo corpus → GitHub /docs")
    parser.add_argument("--dry-run", action="store_true",
                        help="Affiche les actions sans télécharger")
    parser.add_argument("--record", type=str, default=None,
                        help="Force le record ID pour l'entrée avec DOI 10.5281/zenodo.XXXX")
    args = parser.parse_args()

    root = Path(__file__).parent
    missing_records = []
    downloaded = 0
    skipped = 0
    failed = 0

    print(f"\n{'='*60}")
    print(f"  Lux Ferox — Synchronisation Zenodo → GitHub")
    print(f"  Mode : {'DRY-RUN' if args.dry_run else 'TÉLÉCHARGEMENT'}")
    print(f"{'='*60}\n")

    for item in CORPUS:
        target = root / item["target"]
        print(f"[{item['layer']}] {item['date']} {item['title'][:50]}")
        print(f"       → {item['target']}")
        print(f"       Épistémique : {item['epi']}")

        if target.exists() and target.stat().st_size > 1000:
            print(f"  ✓ Déjà présent ({target.stat().st_size // 1024} KB) — skip")
            skipped += 1
            print()
            continue

        record_id = item.get("record")
        if not record_id:
            print(f"  ⚠ record_id manquant — renseigne CORPUS['{item['date']}']['record']")
            missing_records.append(item)
            failed += 1
            print()
            continue

        url = zenodo_url(record_id)
        if not url:
            failed += 1
            print()
            continue

        ok = download_pdf(url, target, dry_run=args.dry_run)
        if ok:
            downloaded += 1
        else:
            failed += 1

        time.sleep(0.5)  # respecter le rate limit Zenodo
        print()

    print(f"{'='*60}")
    print(f"  Résultat : {downloaded} téléchargés · {skipped} déjà présents · {failed} échecs")
    if missing_records:
        print(f"\n  {len(missing_records)} entrées sans record_id :")
        for m in missing_records:
            print(f"    - [{m['date']}] {m['title'][:50]}")
        print("\n  → Va sur https://zenodo.org/search?q=lux+ferox")
        print("    et renseigne le champ 'record' dans CORPUS (ligne ~XX de sync_zenodo.py)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
