# NOV-Discovery-Core

In silico pipeline exploring candidate CYP51 inhibitors against *Naegleria fowleri*
(causative agent of primary amoebic meningoencephalitis, PAM).

📄 Preprint: [ChemRxiv, DOI: 10.26434/chemrxiv.10001710](https://doi.org/10.26434/chemrxiv.10001710)

## Pipeline

- **`generate/`** — candidate SMILES generation via a local LLM (Ollama, qwen2.5:3b),
  filtered by RDKit-based druglikeness rules (MW, LogP, H-bond donors/acceptors), a
  synthetic accessibility score, a basic pharmacophore constraint (azole-like nitrogen
  for heme-iron coordination), and PubChem novelty checks
- **`check/`** — 3D structure preparation (OpenBabel) and molecular docking against
  *N. fowleri* CYP51 (PDB 6AYC, in complex with itraconazole) using AutoDock Vina,
  with post-docking filtering by score and heme-iron distance
- **`results/`** — the final candidate discussed in the preprint, NOV-24

## Requirements

- Python packages: see `requirements.txt`
- [Ollama](https://ollama.com) running locally with the `qwen2.5:3b` model pulled
  (`ollama pull qwen2.5:3b`) — required for `generate/generate.py`
- AutoDock Vina and OpenBabel installed separately (not pip packages)

## Status

This is a working but rough research pipeline, not a polished tool — some scripts are
exploratory and were run manually rather than as a single automated flow. The final
candidate, NOV-24, was selected by hand from generated candidates after applying
chemical filters; generation itself is stochastic, so re-running won't reproduce
the exact same output.

`generate/sascorer.py` and `fpscores.pkl.gz` are third-party code (RDKit/Novartis,
2013) — see `generate/fpscores.SOURCE.txt`.

ADME/pharmacokinetic profiling (SwissADME) was done via the web tool and is not
scripted here — see the preprint for those results.

## Author

Independent high-school research project. AI tools were used throughout as a
learning aid during development and analysis.
