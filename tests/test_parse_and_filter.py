import pandas as pd
from parse_and_filter import apply_lipinski_filter, rank_by_affinity, flag_hits


def test_apply_lipinski_filter_keeps_only_passing_compounds():
    df = pd.DataFrame({
        "compound_name": ["A", "B", "C"],
        "passes_lipinski": [True, False, True],
    })
    result = apply_lipinski_filter(df)
    assert list(result["compound_name"]) == ["A", "C"]


def test_rank_by_affinity_sorts_ascending_and_assigns_rank():
    df = pd.DataFrame({
        "compound_name": ["A", "B", "C"],
        "binding_affinity_kcal_mol": [-5.0, -8.0, -6.5],
    })
    ranked = rank_by_affinity(df)
    assert list(ranked["compound_name"]) == ["B", "C", "A"]
    assert list(ranked["rank"]) == [1, 2, 3]


def test_flag_hits_marks_compounds_at_or_below_threshold():
    df = pd.DataFrame({
        "compound_name": ["A", "B"],
        "binding_affinity_kcal_mol": [-7.0, -4.0],
    })
    flagged = flag_hits(df, threshold=-6.0)
    assert list(flagged["is_hit"]) == [True, False]
