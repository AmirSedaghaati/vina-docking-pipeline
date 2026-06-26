# Vina Docking Pipeline

This automated pipeline is designed to parse, filter and rank theAuto Dock Vina docking results obtained from virtual screening.

## Background

For post-processing large library docking with AutoDock Vina we require obtaining binding affinities and checking against lipinski's rule of 5 and ordering the hits. Repeating this manually on a hundred compounds would be very tedious, error prone, and become a bottle neck in the lead discovery phase.

## Implementation

The parseandfilter.py script automates this:

1. Takes docking output from an appropriately formatted CSV file (binding affinities, Lipinski parameters).
2. Uses a pre-computed "Rule of Five flag" to filter out non-drug-like molecules.
3. Sorts the molecules by binding affinity (more negative binding affinity means tighter binding)
4. Flags "hits" to an user-defined binding affinity threshold.
5. Writes out a ranked summary table and a bar chart of binding affinities.

## Technical Stack

| Component | Function |
|---|---|
| Python 3.10+ | Core data processing |
| pandas | Tabular data manipulation and ranking |
| matplotlib | Visualization of binding affinities |

## Usage

Run from the repository root:

```bash
pip install -r requirements.txt

python parse_and_filter.py --input data/mock_data/docking_results.csv --results results/
```

## Mock Data

`data/mock_data/docking_results.csv` is a synthetic dataset generated to
exercise the pipeline end-to-end. The compound names are real natural-product
molecules commonly used in docking-study examples; the binding-affinity
values are fabricated for demonstration purposes and do not correspond to
any actual docking run, published or unpublished.

## File Structure

```
vina-docking-pipeline/
│
├── data/
│   └── mock_data/
│       └── docking_results.csv     # Illustrative docking results for testing
│
├── results/                        # Output folder (generated on execution)
│   ├── ranked_hits.csv
│   └── affinity_chart.png
│
├── parse_and_filter.py             # Main pipeline script
├── .gitignore
├── requirements.txt
└── README.md
```
## Example output

```bash
python parse_and_filter.py --input data/mock_data/docking_results.csv --results results/