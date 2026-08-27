# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Implements Panama's electoral formula (2024 electoral law) for assigning "Diputados" (deputy) seats
in multi-member ("plurinominal") electoral circuits, from raw vote-count CSVs. It computes cociente,
mediocociente, and residuo (D'Hondt-style largest-remainder) seat allocations and picks the winning
candidate per party for each allocated seat.

## Setup and running

```bash
python3 -m venv .env
source .env/bin/activate
pip install jupyter pandas openpyxl
jupyter notebook
```

There is no build, lint, or test tooling in this repo — no test suite exists. The primary "run" path is
editing and executing `escrutinio.ipynb` (in Jupyter or VS Code), not running a script from the CLI.

To process a circuit:
1. Drop the two escrutinio CSVs for the circuit into `data/` (see naming convention below).
2. In `escrutinio.ipynb`, set `CURULES` (seat count for the circuit) and the two CSV filenames.
3. Run all notebook cells. The final cell writes results to `resultados/`.

## Architecture

The computation is a strict three-stage pipeline over two input tables, wired together in
`escrutinio.ipynb` (the notebook is the entry point/orchestrator — the `escrutinio/` package has no
`main`):

1. **`escrutinio/cocientes.py`** — `nominas_con_curul(primer_escrutinio, curules)` computes the
   cociente (`total_votos / curules`) and mediocociente (`cociente / 2`), then determines which
   *nóminas* (party lists) win seats by cociente (can win multiple) and mediocociente (at most one,
   only for parties with no cociente seat). Operates on the **first escrutinio** (votes totaled by
   nómina/party list). Then `seleccion_de_curul(...)` maps each won seat to a specific candidate from
   the **second escrutinio** (votes totaled by individual candidate), picking the highest-vote
   non-"R" candidate not already selected.
2. **`escrutinio/escrutinio_individual.py`** — `escrutinio_individual(escrutinio)` takes the second
   escrutinio and folds "R" ("Diputados R") rows into the coalition partner they ran with, producing one
   `VotoIndividual` per real candidate with `is_coalition` set when R-votes were merged in. R votes are
   matched to a candidate by name *and* coalition (via `constants/coaliciones.py`), so two same-named
   candidates running in different coalitions don't have their R votes mixed up.
3. **`escrutinio/residuos.py`** — `residuos(votos_individuales, ya_electos, total_curules)` fills any
   remaining seats by largest remainder: highest individual vote count wins, skipping candidates already
   elected and parties that already won a residuo seat, until `total_curules` is reached.

Results from stages 1 and 3 (`list[Resultado]`) are concatenated for the final seat list; stage 2's
output feeds stage 3.

`escrutinio/types.py` defines the shared dataclasses (`Resultado`, `VotoIndividual`, `NominasAsignadas`)
and the `TipoDeSeleccion` enum (COCIENTE / MEDIOCOCIENTE / RESIDUO) threaded through all three stages.

`constants/partidos.py`, `constants/coaliciones.py`, and `constants/plurinominales.py` are static
reference data (party ID → name, coalition membership, which provinces/circuits are plurinominal),
sourced from Electoral Tribunal PDFs and Wikipedia (see docstrings in those files) — not derived from
the vote data.

### Data conventions

- CSV files in `data/` follow `<primer|segundo>_escrutinio_<circuito>.csv` (e.g.
  `primer_escrutinio_8-4.csv`); circuit IDs are `provincia-circuito` (e.g. `8-4`).
- **Primer escrutinio**: totals per nómina (party list) — columns include `Partido`, `Votos`.
- **Segundo escrutinio**: totals per individual candidate — columns include `Partido`, `Nombre`,
  `Votos`, `Es R` (string `"R"`/other in CSV; the notebook converts this to bool before use).
- Party IDs are integers matched against `constants/partidos.py`; there is no canonical candidate ID —
  candidates are identified by ballot name (see README limitations).

## Known limitations (see README.md)

- Coalition vote handling ("Votos de Coalición") and "R" seat assignment are manual/partially modeled;
  "Diputados R" are not assigned automatically and must be marked in the source data by hand.
- Candidate identity is by ballot name only, since the Electoral Tribunal doesn't publish a stable
  candidate ID — two same-named candidates in the *same* coalition would still collide (R votes are
  disambiguated by coalition, not by a unique candidate ID).
- The formula is designed for the 2024 election law; 2019 data is used for testing but predates the
  "Votos de Coalición"/"Diputados R" concepts.
