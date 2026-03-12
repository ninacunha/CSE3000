import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """

    quasi_identifiers = [col for col in anon_df.columns if col in aux_df.columns]
    merged = anon_df.merge(aux_df, on=quasi_identifiers, how="inner")
    counts = merged["anon_id"].value_counts()
    unique_ids = counts[counts == 1].index
    merged = merged[merged["anon_id"].isin(unique_ids)]
 
    merged = merged.rename(columns={"name": "matched_name"})
    return merged[["anon_id", "matched_name"]].reset_index(drop=True)
    # raise NotImplementedError


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    return len(matches_df) / len(anon_df)
    # raise NotImplementedError
