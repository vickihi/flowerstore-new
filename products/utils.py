def compute_average_rating_stats(
    average_rating: float | None,
) -> tuple[float, int, bool]:
    """Return rating display stats as (raw_average, full_stars, has_half_star)."""
    average_rating_value = float(average_rating or 0)
    average_rating_rounded = round(average_rating_value * 2) / 2
    average_rating_full = int(average_rating_rounded)
    average_rating_half = (average_rating_rounded - average_rating_full) == 0.5
    return average_rating_value, average_rating_full, average_rating_half
