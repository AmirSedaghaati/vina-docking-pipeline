import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

# --- Configuration ---
# Threshold chosen based on standard hit-selection criteria for this
# compound class. Adjust if your target or library differs.
AFFINITY_THRESHOLD = -6.0   # kcal/mol — compounds at or below this are hits


def load_results(filepath):
    """Read the docking results CSV into a DataFrame."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} compounds from {filepath}")
    return df


def apply_lipinski_filter(df):
    """
    Keep only compounds that pass Lipinski's Rule of Five.

    The 'passes_lipinski' column is pre-calculated during library
    preparation (e.g. using RDKit); this function filters on that flag.
    """
    before = len(df)
    df_filtered = df[df["passes_lipinski"] == True].copy()
    after = len(df_filtered)
    print(f"Lipinski filter: {before} -> {after} compounds retained")
    return df_filtered


def rank_by_affinity(df):
    """
    Sort compounds by binding affinity (most negative = tightest binding).

    Expects df to already be Lipinski-filtered; ranking the unfiltered
    set would include compounds later removed by apply_lipinski_filter.
    """
    df_ranked = df.sort_values("binding_affinity_kcal_mol", ascending=True).reset_index(drop=True)
    df_ranked["rank"] = df_ranked.index + 1
    return df_ranked


def flag_hits(df, threshold):
    """Mark compounds with affinity at or below the threshold as hits."""
    df = df.copy()
    df["is_hit"] = df["binding_affinity_kcal_mol"] <= threshold
    n_hits = df["is_hit"].sum()
    print(f"Compounds with affinity <= {threshold} kcal/mol: {n_hits}")
    return df


def save_summary(df, output_path):
    """Save the ranked, filtered table to CSV."""
    cols = ["rank", "compound_name", "binding_affinity_kcal_mol",
            "rmsd_lower", "rmsd_upper", "mw_da", "is_hit"]
    df[cols].to_csv(output_path, index=False)
    print(f"Summary saved to {output_path}")


def plot_affinity(df, output_path):
    """
    Bar chart of binding affinities, ranked. Compounds flagged as hits
    (affinity at or below AFFINITY_THRESHOLD) are highlighted.
    """
    colors = ["#c0392b" if hit else "#7f8c8d" for hit in df["is_hit"]]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df["compound_name"], df["binding_affinity_kcal_mol"], color=colors)
    ax.axhline(y=AFFINITY_THRESHOLD, color="black", linestyle="--", linewidth=0.8,
               label=f"Hit threshold ({AFFINITY_THRESHOLD} kcal/mol)")
    ax.set_xlabel("Compound")
    ax.set_ylabel("Binding Affinity (kcal/mol)")
    ax.set_title("AutoDock Vina - Ranked Docking Results")
    ax.legend()
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Plot saved to {output_path}")
    plt.close()


def main(input_file, results_dir):
    os.makedirs(results_dir, exist_ok=True)

    df = load_results(input_file)
    df = apply_lipinski_filter(df)

    if df.empty:
        print("No compounds passed the Lipinski filter. Exiting.")
        return

    df = rank_by_affinity(df)
    df = flag_hits(df, AFFINITY_THRESHOLD)

    save_summary(df, os.path.join(results_dir, "ranked_hits.csv"))
    plot_affinity(df, os.path.join(results_dir, "affinity_chart.png"))

    print("\nTop hits:")
    print(df[df["is_hit"]][["rank", "compound_name", "binding_affinity_kcal_mol"]].to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter and rank AutoDock Vina docking results.")
    parser.add_argument("--input", default="data/mock_data/docking_results.csv",
                        help="Path to docking results CSV")
    parser.add_argument("--results", default="results/",
                        help="Directory to save output files")
    args = parser.parse_args()
    main(args.input, args.results)
