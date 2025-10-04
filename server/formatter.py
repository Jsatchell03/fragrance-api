# formatter.py
import pandas as pd


def format_recommendations(rows: pd.DataFrame) -> str:
    """
    Expect a DataFrame with 3 rows and the columns used above.
    Return a single plain-text block (no JSON) describing each perfume.
    """
    parts = ["Here are three perfumes and their details:"]
    for i, r in enumerate(rows.itertuples(index=False), start=1):
        # Year may be float (e.g., 2000.0) or NaN
        year = getattr(r, "Year")
        year_str = f", {int(year)}" if pd.notna(year) else ""
        rating_val = str(getattr(r, "Rating Value", "")).replace(",", ".")
        rating_cnt = getattr(r, "Rating Count", None)
        rating_str = (
            f"{float(rating_val):.2f} ⭐ ({int(rating_cnt)} ratings)"
            if rating_val and rating_val != "nan" and pd.notna(rating_cnt)
            else "No rating"
        )
        accords = ", ".join(
            [getattr(r, "mainaccord1", None), getattr(r, "mainaccord2", None),
             getattr(r, "mainaccord3", None), getattr(r, "mainaccord4", None),
             getattr(r, "mainaccord5", None)]
        ).replace(", None", "").strip(", ")

        block = (
            f"\n{i}. {r.Perfume.title()} ({r.Brand.title()}, {r.Country}{year_str})\n"
            f"- Gender: {str(r.Gender).capitalize()}\n"
            f"- Rating: {rating_str}\n"
            f"- Top notes: {r.Top or '—'}\n"
            f"- Heart notes: {r.Middle or '—'}\n"
            f"- Base notes: {r.Base or '—'}\n"
            f"- Perfumer(s): "
            f"{' & '.join([p for p in [getattr(r, 'Perfumer1', None), getattr(r, 'Perfumer2', None)] if p and str(p).lower() != 'unknown']) or 'Unknown'}\n"
            f"- Main accords: {accords or '—'}"
        )
        parts.append(block)
    return "\n".join(parts)
